#-------------------------------------------------------------------------------
# Name:        disk
# Purpose:
#
# Author:      Eugene
#
# Created:     06/12/2011
# Copyright:   (c) Eugene 2011
# Licence:     -
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys
import wmi, win32file, win32con, win32api, winioctlcon

platform = sys.platform

class Disk:
    def __init__(self, deviceId):
        self.deviceId = deviceId

    def __str__(self):
        return self.deviceId

    def unmount(self):
        {'win32': self.unmountWin32,
         'linux2': self.unmountLinux,
         'darwin': self.unmountOSX,
        }.get(platform, self.unmountUnknown)()


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

    def unmountLinux(self):
        """Unmount for Linux"""
        pass

    def unmountOSX(self):
        """Unmount for OSX"""
        pass

    def unmountUnknown(self):
        """Unmount for Linux"""
        pass


class DiskEnumerator:
    def __init__(self):
        self.diskDict = {}
        {'win32': self.enumWin32,
         'linux2': self.enumLinux,
         'darwin': self.enumOSX,
        }.get(platform, self.enumUnknown)()

    def __str__(self):
        return str(self.diskDict.keys())

    def __getitem__(self, deviceId):
        """return disk object given its device id"""
        return self.diskDict.get(deviceId)

    def __len__(self):
        return len(self.diskDict)

    def __iter__(self):
        self.keys = sorted(self.diskDict.keys())
        self.index = 0
        return self

    def next(self):
        if self.index >= len(self.keys):
            raise StopIteration
        self.index = self.index + 1
        return self.diskDict[self.keys[self.index-1]]

    def enumWin32(self):
        """Enumeration for Win32"""
        wql = "SELECT * FROM Win32_DiskDrive"
        c = wmi.WMI()
        for disk_drive in c.query(wql):
            disk = Disk(disk_drive.DeviceId)
            disk.model = disk_drive.Model
            disk.serial = disk_drive.SerialNumber
            disk.firmwareRevision = disk_drive.FirmwareRevision
            disk.interfaceType = disk_drive.InterfaceType
            disk.totalCylinders = disk_drive.TotalCylinders
            disk.totalHead = disk_drive.TotalHeads
            disk.sector = disk_drive.SectorsPerTrack
            disk.bytesPerSector = disk_drive.BytesPerSector
            disk.mediaType = disk_drive.MediaType
            for partition in disk_drive.associators ("Win32_DiskDriveToDiskPartition"):
                disk.totalSector = int(partition.NumberOfBlocks)
                disk.size = partition.Size
            self.diskDict[disk_drive.DeviceId] = disk

    def enumLinux(self):
        """Enumeration for Linux"""
        pass

    def enumOSX(self):
        """Enumeration for OSX"""
        pass

    def enumUnknown(self):
        """Enumeration for Linux"""
        pass

def main():
    diskDict = DiskEnumerator()
    for disk in diskDict:
        print disk.model

if __name__ == "__main__":
    main()