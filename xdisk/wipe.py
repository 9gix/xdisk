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

import os, numpy, threading
from Queue import Queue



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

    def compareSectorData(self, sector, value):
        """match value with the sector given. return True if the same"""
        size = len(value)
        self.f.seek(-size,os.SEEK_CUR)
        buff = self.f.read(size)
        if (value == buff):
            return True
        else:
            print "VERIFY FAIL BETWEEN SECTOR %s TO %s" %(sector, sector + self.chunks)
            return False


    def random(self, verify=False):
        randomWorker = RandomWorker(self.sectorSize, self.chunks)
        def writeRandom():
            randomWorker.start()
            for sector in range(0, self.totalSector - self.leftover, self.chunks):
                buff = randomWorker.qBuffer.get()
                self.f.write(buff)
                if verify: self.compareSectorData(sector,buff)
            buff = numpy.random.bytes(512* self.leftover)
            self.f.write(buff)
            if verify: self.compareSectorData(sector,buff)
        return writeRandom

    def fill(self, value=b'\x00', verify=False):
        def writeValue():
            buff = (value*self.chunks*self.sectorSize)[:self.chunks*self.sectorSize]
            for sector in range(0, self.totalSector - self.leftover, self.chunks ):
                self.f.write(buff.encode('latin1'))
                if verify: self.compareSectorData(sector,buff)
            buff = (value*self.leftover*self.sectorSize)[:self.leftover*self.sectorSize]
            self.f.write(buff.encode('latin1'))
            if verify: self.compareSectorData(sector,buff)
        return writeValue

def main():
    from disk import Disk

    disk = Disk("\\\\.\\PhysicalDrive1")
    wiper = Wiper(disk)
    pattern = [wiper.random(),wiper.fill(), wiper.random(True),wiper.fill(b'\xFF',True)]
    wiper.wipe(pattern)
    #disk.unmount()
    #wiper = WiperAlgorithm(disk)

    #wiper.wipePTG()
    #wiper.wipeCustom()

def performance_test():
    import timeit
    #t = timeit.Timer('wiper.wipeCustom()','from __main__ import WiperAlgorithm, Disk; wiper = WiperAlgorithm(Disk("\\\\\.\\\PhysicalDrive1"))')
    #print t.timeit(1)

if __name__ == "__main__":
    main()
    #performance_test()