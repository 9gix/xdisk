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
from disk import Disk


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

def main():
    disk = Disk("\\\\.\\PhysicalDrive1")
    #disk.unmount()
    #wiper = WiperAlgorithm(disk)

    #wiper.wipePTG()
    #wiper.wipeCustom()

def performance_test():
    import timeit
    #t = timeit.Timer('wiper.wipeCustom()','from __main__ import WiperAlgorithm, Disk; wiper = WiperAlgorithm(Disk("\\\\\.\\\PhysicalDrive1"))')
    #print t.timeit(1)

if __name__ == "__main__":
    #main()
    performance_test()