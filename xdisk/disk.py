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
    """Attribute will be filled only from Disk Enumerator class"""
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
        wql = "SELECT * FROM Win32_DiskDrive"
        c = wmi.WMI()
        win32DiskDriveDict = {}

        # Win32_DiskDrive Instance
        for diskDrive in c.query(wql):
            diskDriveDict = {}
            diskDriveDict[u"DiskPartition"] = []
            win32DiskDriveDict[diskDrive.DeviceID] = diskDriveDict

            # Win32_DiskDrive Properties
            for propertyName in sorted(list(diskDrive.properties)):
                diskDriveDict[propertyName] = getattr(diskDrive, propertyName,'')

            # Win32_DiskPartition Instance
            for diskPartition in sorted(list(diskDrive.associators("Win32_DiskDriveToDiskPartition"))):
                diskPartitionDict = {}
                diskPartitionDict[u"LogicalDisk"] = []
                diskDriveDict[u"DiskPartition"].append(diskPartitionDict)

                # Win32_DiskPartition Properties
                for propertyName in sorted(list(diskPartition.properties)):
                    diskPartitionDict[propertyName] = getattr(diskPartition, propertyName,'')

                # Win32_LogicalDisk Instance
                for logicalDisk in sorted(list(diskPartition.associators ("Win32_LogicalDiskToPartition"))):
                    partitionDict = {}
                    diskPartitionDict[u"LogicalDisk"].append(partitionDict)

                    # Win32_LogicalDisk Properties
                    for propertyName in sorted(list(logicalDisk.properties)):
                        partitionDict[propertyName] = getattr(logicalDisk,propertyName,'')
        #pprint(win32DiskDriveDict)										
				
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