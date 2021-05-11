import os
import ROOT
import json

class Hist(ROOT.TH1):
    def __init__(self, name, phyObject, selection, dataset, tree):
        self.name = name
        self.phyObject = phyObject
        self.selection = selection
        self.histName = "{}_{}_{}".format(phyObject, selection, name)
        self.dataset = dataset
        self.tree = tree
    
    def getTH1Parameters(self):
        histParasDict = {'M': {'RecDiMuon': '60, 75, 105', 'RecDiJet': '75, 50, 200'}, 'Pt':'50, 0, 500', 'Eta':'60, -6, 6', 'Phi':'40, -4, 4'}
        loopFlag = False
        for kinimatic, para in histParasDict.items():
            if kinimatic == self.name:
                loopFlag = True
                histEdge = para
                if self.name == 'M':
                    histEdge = para[self.phyObject]
        if loopFlag == False: 
            print('You input wrong physical object!')
        self.histPara = histEdge
    
    def getScaleFactor(self):
        with open('MCInfo.json') as mcInfo:
            mcInfoList = json.load(mcInfo)

        
    def getHist(self):
        self.tree.Draw("{} >> {}({})") # nbins, xmin, xmax in the bracket
        h = ROOT.gROOT.FindObject()
