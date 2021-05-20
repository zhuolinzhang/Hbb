import os
import ROOT
import plotConfig
import plotHelper

def genCategoryHist(onlySampleCateList, phyObjList, selectKineDict, includeData=True):
    global genCategoryHist
    histEdgeDict = {'M': {'RecDiMuon': '60, 75, 105', 'RecDiJet': '75, 50, 200'}, 'Pt':'50, 0, 500', 'Eta':'60, -6, 6', 'Phi':'40, -4, 4'}
    if includeData == True: 
        sampleCateList = onlySampleCateList
        sampleCateList.append('data')
    for k in selectKineDict.values():
        for s in selectKineDict.keys():
            for phyObj in phyObjList:
                for sample in sampleCateList:
                    if k == 'M':
                        histEdge = histEdgeDict['M'][phyObj]
                    else:
                        histEdge = histEdgeDict[k]
                    exec('{0}_{1}_{2}_{3} = ROOT.TH1F("{0}_{1}_{2}_{3}", "{0}_{1}_{2}_{3}", {4})'.format(sample, phyObj, s, k, histEdge))

def categoryHists(sampleCateList, hist):
    global categoryHists
    for sample in sampleCateList:
        if hist.mcCategory == sample:
            exec('{}_{}_{}_{} += {}'.format(sample, hist.phyObject, hist.selection, hist.kinematics, hist.hist))
        elif hist.mcCategory == 'data':
            exec('data_{0}_{1}_{2} += {3}'.format(hist.phyObject, hist.selection, hist.kinematics, hist.hist))

def getHistsFromTree(tree, datasetName, phyObjList, selectKineDict, sampleList):
    global getHistsFromTree
    for phyObj in phyObjList:
        for select, kine in selectKineDict.items():
            for s in select:
                for k in kine:
                    exec('h_{0}_{1}_{2} = plotConfig.Hist({2}, {0}, {1}, {3}, {4})'.format(phyObj, s, k, datasetName, tree))
                    exec('categoryHists({3}, h_{0}_{1}_{2})'.format(phyObj, s, k, sampleList)) 

sampleCategoryList = ['zh', 'st', 'tt', 'dib', 'qcd', 'zjets']
phyObjList = ['RecDiMuon', 'RecDiJet']
selectKineDict = {'Match': ['Pt', 'Eta', 'Phi', 'M']}

genCategoryHist(sampleCategoryList, phyObjList, selectKineDict)
fileList = plotHelper.openRootFiles("./dataset")
for file in fileList:
    zhTree = file.Get("ZHCandidates")
    datasetPrimaryName = plotHelper.getPrimaryName(file)
    getHistsFromTree(zhTree, datasetPrimaryName, phyObjList, selectKineDict, sampleCategoryList)

