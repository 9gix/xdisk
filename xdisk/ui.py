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

    def enumAlgorithm(self):
        self.algorithmList = []

    def craftAlgorithm(self,name,description,*methodList):
        pass

    def wipeDisk(self,diskList,method):
        for disk in diskList:
            wiper = WiperAlgorithm(disk)


#-------------------------------------------------------------------------------
import Tkinter
import tkFont

class AlgorithmView(Tkinter.Toplevel):
    def __init__(self):
        Tkinter.Toplevel.__init__(self)


class View(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.geometry("640x480")
        monospace = tkFont.Font(family='Courier',size=9)

        self.diskList = Tkinter.Listbox(self,selectmode=Tkinter.EXTENDED)
        self.diskList.grid(row=0,column=0,sticky=Tkinter.NSEW)
        self.detectBtn = Tkinter.Button(self,text='Detect')
        self.detectBtn.grid(row=1,column=0,sticky=Tkinter.NSEW)
        self.diskInfo = Tkinter.Listbox(self,font=monospace)
        self.diskInfo.grid(row=0,column=1,rowspan=2,sticky=Tkinter.NSEW)
        self.wipeBtn = Tkinter.Button(self,text='Wipe')
        self.wipeBtn.grid(row=2,column=1,sticky=Tkinter.NSEW)

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0)
        self.columnconfigure(1,weight=2)


#-------------------------------------------------------------------------------
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.view.detectBtn.config(command=self.detectDisk)
        self.view.wipeBtn.config(command=self.wipeDisk)
        self.view.diskList.bind("<<ListboxSelect>>", self.diskListSelected)

        self.view.mainloop()

    def detectDisk(self):
        self.model.enumDisk()
        self.view.diskList.delete(0,Tkinter.END)
        self.view.diskList.insert(Tkinter.END,*self.model.diskList)

    def diskListSelected(self,event):
        selection = event.widget.curselection()
        selectedList = [self.view.diskList.get(int(item)) for item in selection]
        self.diskSelected = [self.model.diskList[deviceId] for deviceId in selectedList]
        self.displayDiskInfo()

    def displayDiskInfo(self):
        def heading(text, padding="-",width=60):
            return '{0:{1}^{2}}'.format(text,padding,width)

        def body(key,value,width=60):
            return '{0: <17} : {1: >40}'.format(k,v)

        self.view.diskInfo.delete(0,Tkinter.END)
        for disk in self.diskSelected:
            self.view.diskInfo.insert(Tkinter.END,heading(disk))
            for k,v in disk.__dict__.iteritems():
                self.view.diskInfo.insert(Tkinter.END, body(k,v))
            self.view.diskInfo.insert(Tkinter.END,"")

    def wipeDisk(self):
        self.model.wipeDisk(self.diskSelected, None)




#-------------------------------------------------------------------------------
def main():
    app = Controller()

if __name__ == '__main__':
    main()
