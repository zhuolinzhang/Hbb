import ROOT
import json

class Hist():
    def __init__(self, kinematics, phyObject, selection, dataset, tree) -> None:
        self.kinematics = kinematics
        self.phyObject = phyObject
        self.selection = selection
        self.histName = "h_{}_{}_{}".format(phyObject, selection, kinematics)
        self.dataset = dataset
        self.tree = tree
        recoTargetDict = {'RecDiMuon': 'Z', 'RecDiJet': 'Higgs'}
        dataList = ['DoubleMuon2018A', 'DoubleMuon2018B', 'DoubleMuon2018C', 'DoubleMuon2018D']
        self.recoObject = recoTargetDict[self.phyObject]
        if dataset in dataList:
            self.mcOrData = 'data'
        else: self.mcOrData = 'mc'
        self.histEdge = self.getTH1Edge()
        self.hist = self.getHist()
        if self.mcOrData == 'data':
            self.mcCategory = 'data'
        else: 
            self.mcCategory = self.getCategoryOfMC()
            self.hist.Scale(self.getScaleFactor())
    
    def getTH1Edge(self):
        histEdgeDict = {'M': {'RecDiMuon': '60, 75, 105', 'RecDiJet': '75, 50, 200'}, 'Pt':'50, 0, 500', 'Eta':'60, -6, 6', 'Phi':'40, -4, 4'}
        loopFlag = False
        for kinimatic, para in histEdgeDict.items():
            if kinimatic == self.kinematics:
                loopFlag = True
                histEdge = para
                if self.kinematics == 'M':
                    histEdge = para[self.phyObject]
        if loopFlag == False: 
            print('You input wrong physical object!')
        return histEdge
    
    def getScaleFactor(self):
        with open('MCInfo_IsoMu20_UL2018.json') as mcInfo:
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
        self.tree.Draw("{}{} >> {}({})".format(self.recoObject, self.kinematics, self.histName, self.histEdge)) # nbins, xmin, xmax in the bracket
        h = ROOT.gROOT.FindObject(self.histName)
        return h
    
    def getCategoryOfMC(self):
        matchDict = {'ZH_HToBB':'zh', 'TTTo':'tt', 'channel':'st', 'ZZ':'zz', 'QCD':'qcd', 'DYJetsToLL':'zjets'}
        mcCategory = None
        for datasetName in matchDict.keys():
            if datasetName in self.dataset:
                mcCategory = matchDict[datasetName]
        if mcCategory == None:
            print("The dataset name {} is wrong! Please check!".format(self.dataset))
        return mcCategory