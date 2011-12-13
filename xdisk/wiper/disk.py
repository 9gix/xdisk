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

class Disk:
    def __init__(self, DeviceID):
        self.DeviceID = DeviceID
    def __repr__(self):
        return self.DeviceID

class DiskEnumerator:
    def __init__(self):
        import sys
        self.diskList = {'win32': self.enumWin32,
         'linux2': self.enumLinux,
         'darwin': self.enumOSX,
        }.get(sys.platform, self.enumUnknown)()

    def __str__(self):
        return str(self.diskList)

    def __getitem__(self, deviceId):
        """return disk object given its device id"""
        return [disk for disk in self if str(disk) in deviceId][0]

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


if __name__ == '__main__':
    main()
