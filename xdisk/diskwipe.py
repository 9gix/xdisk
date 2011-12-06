#-------------------------------------------------------------------------------
# Name:        diskwipe
# Purpose:
#
# Author:      Eugene
#
# Created:     06/12/2011
# Copyright:   (c) Eugene 2011
# Licence:     -
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import wmi, os, sys, numpy, threading
import win32file, win32con, win32api, winioctlcon
from Queue import Queue

platform = sys.platform


class Disk:
    def __init__(self, deviceId):
        self.deviceId = deviceId

        # Enumerate Disk Information Based on Its Operating System
        {'win32': self.enumWin32,
         'linux2': self.enumLinux,
         'darwin': self.enumOSX,
        }.get(platform, self.enumUnknown)()

    def unmount(self):
        {'win32': self.unmountWin32,
         'linux2': self.unmountLinux,
         'darwin': self.unmountOSX,
        }.get(platform, self.unmountUnknown)()

    def enumWin32(self):
        """Enumeration for Win32"""
        wql = "SELECT * FROM Win32_DiskDrive WHERE DeviceID = '%s'"%self.deviceId
        c = wmi.WMI()
        for disk in c.query(wql):
            self.model = disk.Model
            self.serial = disk.SerialNumber
            self.firmwareRevision = disk.FirmwareRevision
            self.interfaceType = disk.InterfaceType
            self.totalCylinders = disk.TotalCylinders
            self.totalHead = disk.TotalHeads
            self.sector = disk.SectorsPerTrack
            self.bytesPerSector = disk.BytesPerSector
            self.mediaType = disk.MediaType
            for partition in disk.associators ("Win32_DiskDriveToDiskPartition"):
                self.totalSector = int(partition.NumberOfBlocks)
                self.size = partition.Size

    def unmountWin32(self):
        """Unmount for Win32"""
        hVol = win32file.CreateFile(
            self.deviceId,
            win32con.GENERIC_READ|win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_WRITE|win32con.FILE_SHARE_READ,
            None,
            win32con.OPEN_EXISTING,
            0,
            None)
        try:
            c = win32file.DeviceIoControl(hVol,winioctlcon.FSCTL_DISMOUNT_VOLUME,None,0)
        except :
            return False
        return True

    def enumLinux(self):
        """Enumeration for Linux"""
        pass

    def unmountLinux(self):
        """Unmount for Linux"""
        pass

    def enumOSX(self):
        """Enumeration for OSX"""
        pass

    def unmountOSX(self):
        """Unmount for OSX"""
        pass

    def enumUnknown(self):
        """Enumeration for Linux"""
        pass

    def unmountUnknown(self):
        """Unmount for Linux"""
        pass

class RandomWorker(threading.Thread):
    def __init__(self, sectorSize, chunks):
        threading.Thread.__init__(self)
        self.sectorSize = sectorSize
        self.chunks = chunks
        self.qBuffer = Queue(10)

    def run(self):
        while True:
            self.qBuffer.put(numpy.random.bytes(self.sectorSize * self.chunks))

class Wiper:

    def __init__(self, disk):
        self.disk = disk
        self.totalSector = 15000 #disk.totalSector
        self.sectorSize = self.disk.bytesPerSector
        self.chunks = ( 2 ** 15 ) / self.sectorSize
        self.leftover = self.totalSector%self.chunks


    def wipe(self,patternList):
        with open(self.disk.deviceId, 'rb+') as self.f:
            for pattern in patternList:
                self.f.seek(0, os.SEEK_SET)
                pattern()

    def random(self, verify=False):
        randomWorker = RandomWorker(self.sectorSize, self.chunks)
        def writeValue():
            randomWorker.start()
            for sector in range(0, self.totalSector - self.leftover, self.chunks):
                buff = randomWorker.qBuffer.get()
                self.f.write(buff)
                if verify:
                    self.f.seek(-512*self.chunks,os.SEEK_CUR)
                    if self.f.read(512*self.chunks) != buff:
                        print "VERIFY FAIL BETWEEN SECTOR %s TO %s" %(sector, sector + chunks)
            buff = numpy.random.bytes(512* self.leftover)
            self.f.write(buff)
        return writeValue

    def _random(self, verify=False):
        def writeValue():
            for sector in range(0, self.totalSector - self.leftover, self.chunks):
                buff = numpy.random.bytes(512 * self.chunks)
                self.f.write(buff)
                if verify:
                    self.f.seek(-512*self.chunks,os.SEEK_CUR)
                    if self.f.read(512*self.chunks) != buff:
                        print "VERIFY FAIL BETWEEN SECTOR %s TO %s" %(sector, sector + chunks)
            self.f.write(numpy.random.bytes(512* self.leftover))
        return writeValue

    def _fill(self, value=b'\x00', verify=False):
        def writeValue():
            buff = (value*self.chunks*self.sectorSize)[:self.chunks*self.sectorSize]
            for sector in range(0, self.totalSector - self.leftover, self.chunks ):
                self.f.write(buff)
            buff = (value*self.leftover*self.sectorSize)[:self.leftover*self.sectorSize]
            self.f.write(buff)
        return writeValue

    def fill(self, value=b'\x00', verify=False):
        def writeValue():
            for sector in range(0, self.totalSector - self.leftover, self.chunks ):
                self.f.write((value*self.chunks*self.sectorSize)[:self.chunks*self.sectorSize])
            self.f.write((value*self.leftover*self.sectorSize)[:self.leftover*self.sectorSize])
        return writeValue

class WiperAlgorithm(Wiper):
    def __init__(self,disk):
        Wiper.__init__(self,disk)

    def wipePTG(self):
        self.ptg = [
            self.random(), self.random(), self.random(), self.random(),
            self.fill(b'\x55'), self.fill(b'\xAA'),
            self.fill(b'\x92\x49\x24'), self.fill(b'\x49\x24\x92'),
            self.fill(b'\x24\x92\x49'),
            self.fill(b'\x00'), self.fill(b'\x11'),
            self.fill(b'\x22'), self.fill(b'\x33'),
            self.fill(b'\x44'), self.fill(b'\x55'),
            self.fill(b'\x66'), self.fill(b'\x77'),
            self.fill(b'\x88'), self.fill(b'\x99'),
            self.fill(b'\xAA'), self.fill(b'\xBB'),
            self.fill(b'\xCC'), self.fill(b'\xDD'),
            self.fill(b'\xEE'), self.fill(b'\xFF'),
            self.fill(b'\x92\x49\x24'), self.fill(b'\x49\x24\x92'),
            self.fill(b'\x24\x92\x49'),
            self.fill(b'\x6d\xb6\xdb'), self.fill(b'\xb6\xdb\x6d'), self.fill(b'\xdb\x6d\xb6'),
            self.random(), self.random(),self.random(), self.random()]
        self.wipe(self.ptg)

    def wipeCustom(self):
        rnd = [self.fill(),self.fill(),self.fill(),
        self.fill(),self.fill(),self.fill(),
        self.fill(),self.fill(),self.fill(),
        self.fill(),self.fill(),self.fill(),
        self.fill(),self.fill(),self.fill(),
        self.fill(),self.fill(),self.fill(),]
        self.wipe(rnd)

def main():
    disk = Disk("\\\\.\\PhysicalDrive1")
    #disk.unmount()
    wiper = WiperAlgorithm(disk)

    wiper.wipePTG()
    #wiper.wipeCustom()

def performance_test():
    import timeit
    t = timeit.Timer('wiper.wipeCustom()','from __main__ import WiperAlgorithm, Disk; wiper = WiperAlgorithm(Disk("\\\\\.\\\PhysicalDrive1"))')
    print t.timeit(1)

if __name__ == "__main__":
    #main()
    performance_test()