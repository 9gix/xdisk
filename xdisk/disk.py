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

import sys
import wmi, win32file, win32con, win32api, winioctlcon

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
