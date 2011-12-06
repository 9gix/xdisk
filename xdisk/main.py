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

from algorithm import WiperAlgorithm
from disk import Disk

def main():
    disk = Disk("\\\\.\\PhysicalDrive1")
    #disk.unmount()
    wiper = WiperAlgorithm(disk)

    wiper.wipePTG()
    #wiper.wipeCustom()

if __name__ == "__main__":
    main()