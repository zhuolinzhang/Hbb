import os
import ROOT
import json

class Hist(ROOT.TH1):
    def __init__(self, kinematics, phyObject, selection, dataset, tree):
        self.kinematics = kinematics
        self.phyObject = phyObject
        self.selection = selection
        self.histName = "h_{}_{}_{}".format(phyObject, selection, kinematics)
        self.dataset = dataset
        self.tree = tree
    
    def getTH1Parameters(self):
        histParasDict = {'M': {'RecDiMuon': '60, 75, 105', 'RecDiJet': '75, 50, 200'}, 'Pt':'50, 0, 500', 'Eta':'60, -6, 6', 'Phi':'40, -4, 4'}
        loopFlag = False
        for kinimatic, para in histParasDict.items():
            if kinimatic == self.kinematics:
                loopFlag = True
                histEdge = para
                if self.kinematics == 'M':
                    histEdge = para[self.phyObject]
        if loopFlag == False: 
            print('You input wrong physical object!')
        self.histPara = histEdge
    
    def getScaleFactor(self):
        with open('MCInfo_IsoMu20.json') as mcInfo:
            mcInfoList = json.load(mcInfo)
        factor = 1
        for eachDataset in mcInfoList:
            for value in eachDataset.values():
                if self.dataset == value:
                    factor = eachDataset["factor_IsoMu20"]
                    break
        if factor == 1: print("Your dataset name is not in the json file!")
        return factor

    def getHist(self):
        self.tree.Draw("{} >> {}({})") # nbins, xmin, xmax in the bracket
        h = ROOT.gROOT.FindObject()
