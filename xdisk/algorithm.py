#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      91315
#
# Created:     06/12/2011
# Copyright:   (c) 91315 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from wipe import Wiper

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
    from disk import Disk
    disk = Disk("\\\\.\\PhysicalDrive1")
    #disk.unmount()
    wiper = WiperAlgorithm(disk)

    wiper.wipePTG()
    #wiper.wipeCustom()

def performance_test():
    import timeit
    #t = timeit.Timer('wiper.wipeCustom()','from __main__ import WiperAlgorithm, from disk import Disk; wiper = WiperAlgorithm(Disk("\\\\\.\\\PhysicalDrive1"))')
    #print t.timeit(1)

if __name__ == "__main__":
    #main()
    performance_test()