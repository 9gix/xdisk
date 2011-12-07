#-------------------------------------------------------------------------------
# Name:        ui
# Purpose:
#
# Author:      Eugene
#
# Created:     07/12/2011
# Copyright:   (c) Eugene 2011
# Licence:     -
#-------------------------------------------------------------------------------
#!/usr/bin/env python
#-------------------------------------------------------------------------------
from disk import DiskEnumerator
from algorithm import WiperAlgorithm

class Model:
    def __init__(self):
        pass

    def enumDisk(self):
        self.diskList = DiskEnumerator()

#-------------------------------------------------------------------------------
import Tkinter

class View(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.diskList = Tkinter.Listbox(self)
        self.diskList.pack()
        self.detectBtn = Tkinter.Button(self,text='Detect')
        self.detectBtn.pack()


#-------------------------------------------------------------------------------
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.view.detectBtn.config(command=self.detectDisk)
        self.view.mainloop()


    def detectDisk(self):
        self.model.enumDisk()
        self.view.diskList.delete(0,Tkinter.END)
        for disk in self.model.diskList:
            self.view.diskList.insert(Tkinter.END,disk)


#-------------------------------------------------------------------------------
def main():
    app = Controller()

if __name__ == '__main__':
    main()
