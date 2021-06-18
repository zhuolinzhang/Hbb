import pandas as pd
import numpy as np
import os
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, help="The path of cutflows")
parser.add_argument("-o", type=str, help="The path of save outputs")
parser.add_argument("--json", type=str, help="The path of json file")
args = parser.parse_args()

def getScaleFactor(jsonPath, txtName):
    with open(jsonPath) as mcInfo:
        mcInfoList = json.load(mcInfo)
    factor = 1
    for eachDataset in mcInfoList:
        for value in eachDataset.values():
            if txtName == value:
                factor = eachDataset["factor_IsoMu20"]
                break
    if factor == 1:
        print("Your dataset name {} is not in the json file!".format(txtName))
    print("{}\tscale factor = {}".format(txtName, factor))
    return factor

def genCategoryDict(datasetList):
    matchHelperDict = {'ZH_HToBB': 'zh', 'TTTo': 'tt', 'channel': 'st', 'ZZ': 'dib', 'QCD': 'qcd', 'DYJetsToLL': 'zjets', 'DoubleMuon': 'data'}
    cateDict = {'zh': [], 'tt': [], 'st': [], 'dib': [], 'qcd': [], 'zjets': [], 'data': []}
    for i in datasetList:
        for key, value in matchHelperDict.items():
            if key in i: 
                cateDict[value].append(i)
    return cateDict

def genTxtList(cutFlowPath):
    folderList = os.listdir(cutFlowPath)
    datasetList = []
    for i in folderList:
        if '.txt' in i:
            datasetList.append(i.rstrip('.txt'))
    return datasetList

def categoryCutFlowDf(path, dataset, jsonPath, cate_df):
    print('Read {}'.format(dataset))
    df = pd.read_csv(path + '/' + dataset + '.txt', delimiter='\t')
    df = df.set_index('Name')
    df = df.fillna(0)
    df = df * getScaleFactor(jsonPath, dataset)
    cate_df = df.loc[:, 'Pass': 'All'] + cate_df
    return cate_df
    
def calcEff(dataFrame, savePath, fileName):
    print("Calculate the effective in {}".format(fileName))
    dataFrame['Eff.(%)'] = dataFrame['Pass'] / dataFrame['All'] * 100.
    dataFrame['Cum. Eff.(%)'] = dataFrame['Pass'] / dataFrame.loc['Muon Pt', 'All'] * 100.
    if os.path.exists(savePath): pass
    else: os.mkdir(savePath)
    dataFrame.to_csv(savePath + '/' + fileName + '.csv')
    dataFrame.to_latex(savePath + '/' + fileName + '.tex')

cutFlowList = genTxtList(args.i)
datasetKindDict = genCategoryDict(cutFlowList)
for i in datasetKindDict.keys():
        exec('df_{} = pd.DataFrame(np.zeros((9, 2)), columns=["Pass", "All"], index=["Muon Pt", "Tight Muon", "Muon Eta", "Muon Iso", "Z Mass", "Jet Pt", "deepCSV", "Jet ID", "Higgs Mass"])'.format(i))
for datasetKind, datasetList in datasetKindDict.items():
    for dataset in datasetList:
        exec('df_{3} = categoryCutFlowDf("{0}", "{1}", "{2}", df_{3})'.format(args.i, dataset, args.json, datasetKind))
for datasetKind in datasetKindDict.keys():
    exec('calcEff(df_{0}, "{1}", "{0}")'.format(datasetKind, args.o))