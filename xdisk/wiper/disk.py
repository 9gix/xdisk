#-------------------------------------------------------------------------------
# Name:        xdisk.wiper.disk
# Purpose:
#
# Author:      Eugene
#
# Created:     13/12/2011
# Copyright:   (c) Eugene 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import sys

class Disk:
    def __init__(self, DeviceID):
        self.DeviceID = DeviceID

    def __repr__(self):
        return self.DeviceID

    def unmount(self):
        return {'win32': self.unmountWin32,
         'linux2': self.unmountLinux,
         'darwin': self.unmountOSX,
        }.get(sys.platform, self.unmountUnknown)()


    def unmountWin32(self):
        """Unmount for Win32"""
        import win32con, win32file, winioctlcon
        hVol = win32file.CreateFile(
            self.DeviceID,
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
        self.diskList = {'win32': self.enumWin32,
         'linux2': self.enumLinux,
         'darwin': self.enumOSX,
        }.get(sys.platform, self.enumUnknown)()

    def __str__(self):
        return str(self.diskList)

    def __getitem__(self, deviceId):
        """return disk object given its device id"""
        try:
            return next(disk for disk in self
                        if str(disk).upper() == deviceId.upper())
        except:
            return None

    def __len__(self):
        return len(self.diskList)

    def __iter__(self):
        self.length = len(self)
        self.index = 0
        return self

    def next(self):
        if self.index < self.length:
            self.index = self.index + 1
            return self.diskList[self.index - 1]
        raise StopIteration

    def enumWin32(self):
        import wmi

        wql = "SELECT * FROM Win32_DiskDrive"
        c = wmi.WMI()
        diskList = []

        # Win32_DiskDrive Instance
        for diskDrive in c.query(wql):
            disk = Disk(diskDrive.DeviceID)
            disk.DiskPartition = []

            # Win32_DiskDrive Properties
            for propertyName in sorted(list(diskDrive.properties)):
                setattr(disk,propertyName,getattr(diskDrive, propertyName,''))

            # Win32_DiskPartition Instance
            for diskPartition in sorted(list(diskDrive.associators("Win32_DiskDriveToDiskPartition"))):
                # Win32_LogicalDisk Instance
                for logicalDisk in sorted(list(diskPartition.associators ("Win32_LogicalDiskToPartition"))):
                    # DiskPartition DeviceID (or Drive Letter)
                    disk.DiskPartition.append(logicalDisk.DeviceID)
            diskList.append(disk)
        return diskList

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
    diskList = DiskEnumerator()
    for disk in diskList:
        print disk
    print diskList["\\\\.\\physicaldrive1"]

if __name__ == '__main__':
    main()
