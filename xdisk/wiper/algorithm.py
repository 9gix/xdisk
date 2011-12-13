#-------------------------------------------------------------------------------
# Name:        xdisk.wiper.algorithm
# Purpose:
#
# Author:      Eugene
#
# Created:     13/12/2011
# Copyright:   (c) Eugene 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

try:
    from .wipe import Wiper
except ValueError:
    from wipe import Wiper

import json

class WiperAlgorithm(Wiper):
    def __init__(self,disk,algo_json='algo.json'):
        Wiper.__init__(self,disk)
        self.algo_json = algo_json

        self.loadAlgo()

    def loadAlgo(self):

        with open(self.algo_json,'r') as f:
            try:
                js = json.load(f)
            except ValueError:
                js = []
        self.algorithmList = []
        for algoDict in js:
            algorithm = {}
            algorithm['name'] = algoDict.get('name')
            algorithm['description'] = algoDict.get('description')
            methodList = []
            for method in algoDict['passes']:
                verify = method.get('verify',False)
                if method.get('fill'):
                    value = method.get('fill',b'\x00')
                    methodList.append(self.fill(value,verify))
                elif method.get('random'):
                    methodList.append(self.random(verify))
            algorithm['methods'] = methodList
            self.algorithmList.append(algorithm)

    def saveAlgo(self,algorithm='My Algorithm',description=None,*method):
        """Save Algorithm as JSON

        method only accept dictionary.
        method key such as:
            random ==> bool
            fill ==> byte or str
            pass ==> int
            verify ==> bool
        """
        with open(self.algo_json,'r') as f:
            try:
                js = json.load(f)
            except ValueError:
                js = []
        algorithmDict = {
            'name':algorithm,
            'description':description,
            'passes':method}
        js.append(algorithmDict)
        with open(self.algo_json,'w') as f:
            f.write(json.dumps(js,encoding='latin1',indent=4,sort_keys=True))

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

def algo2json(wiper):
    ptg = ("Peter Gutmann",None,
        {'random':True},{'random':True},{'random':True},{'random':True},
        {'fill':b'\x55'},{'fill':b'\xAA'},
        {'fill':b'\x92\x49\x24'},{'fill':b'\x49\x24\x92'},{'fill':b'\x24\x92\x49'},
        {'fill':b'\x00'},{'fill':b'\x11'},
        {'fill':b'\x22'},{'fill':b'\x33'},
        {'fill':b'\x44'},{'fill':b'\x55'},
        {'fill':b'\x66'},{'fill':b'\x77'},
        {'fill':b'\x88'},{'fill':b'\x99'},
        {'fill':b'\xAA'},{'fill':b'\xBB'},
        {'fill':b'\xCC'},{'fill':b'\xDD'},
        {'fill':b'\xEE'},{'fill':b'\xFF'},
        {'fill':b'\x92\x49\x24'},{'fill':b'\x49\x24\x92'},{'fill':b'\x24\x92\x49'},
        {'fill':b'\x6d\xb6\xdb'},{'fill':b'\xb6\xdb\x6d'},{'fill':b'\xdb\x6d\xb6'},
        {'random':True},{'random':True},{'random':True},{'random':True},
        )

    algo = ptg
    wiper.saveAlgo(*algo)

def main():
    from disk import Disk, DiskEnumerator

    diskList = DiskEnumerator()
    disk = diskList['\\\\.\\PHYSICALDRIVE1']

    #disk.unmount()
    wiper = WiperAlgorithm(disk)
    #algo2json(wiper)

    wiper.wipe(wiper.algorithmList[0]['methods'])
    #wiper.wipePTG()
    #wiper.wipeCustom()

if __name__ == "__main__":
    main()