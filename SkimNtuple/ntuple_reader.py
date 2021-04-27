import ROOT
import os
import FileIO
import re

filePath = "./ZHNtupleTest1_210316"
if not(os.path.exists("Output")):
    os.mkdir("Output")
rooList = FileIO.open_file(filePath)
histTreeDict = {}
# Generate histogram dictionary
kinDict = {"Mass": "M", "Pt": "pt", "Eta": "eta", "Phi": "phi"}
particleDict = {"Z": "RecDiMuon", "Higgs": "RecDiJet"}
for k1, v1 in particleDict.items():
    for k2, v2 in kinDict.items():
        exec("histTreeDict['{}{}'] = 'h_{}_Match_{}'".format(k1, k2, v1, v2))
histBinsPrimaryDict = {'RecDiMuon_Match_M': '60, 75, 105', 'RecDiJet_Match_M': '75, 50, 200', '_pt':'50, 0, 500', '_eta':'60, -6, 6', '_phi':'40, -4, 4'}
histBinsDict = {}
for k1, v1 in histBinsPrimaryDict.items():
    for v2 in histTreeDict.values():
        if re.search(k1, v2):
            exec("histBinsDict['{}'] = '{}'".format(v2, v1))
# read TTree
ZHTree = ROOT.TTree()
for i in rooList:
    ZHTree = i.Get("demo/ZHCandidates")
    if ZHTree.GetEntries() == 0: continue
    rooFileName = FileIO.get_primary_name(rooList.index(i), filePath)
    print("Read {}".format(rooFileName))
    fOutput = ROOT.TFile("./Output/{}.root".format(rooFileName), "RECREATE")
    for key, value in histTreeDict.items():
        ZHTree.Draw("{} >> {}({})".format(key, value, histBinsDict[value]))
        exec('{0} = ROOT.gROOT.FindObject("{0}")'.format(value))
        exec('{}.Write()'.format(value))
