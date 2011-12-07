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

    def detectDisk(self):
        pass


#-------------------------------------------------------------------------------
import Tkinter

class View(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)


#-------------------------------------------------------------------------------
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.view.mainloop()


#-------------------------------------------------------------------------------
def main():
    app = Controller()

if __name__ == '__main__':
    main()
