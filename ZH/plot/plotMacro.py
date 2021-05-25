import os
import ROOT
import plotConfig
import plotHelper
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, help="mcData or srSideband The type of THStack")
args = parser.parse_args()

def checkEnv(stackType, sidebandDataset, SRDataset, output):
    if os.path.exists(sidebandDataset): 
        print("Sideband dataset folder exist.")
    else: 
        raise SystemExit("The sideband dataset folder doesn't exist! Please check!")
    if stackType == 'srSideband':
        if os.path.exists(SRDataset): 
            print("Signal region dataset folder exist.")
        else: 
            raise SystemExit("The signal region dataset folder doesn't exist! Please check!")
    if os.path.exists(output): pass
    else: os.mkdir(output)

sampleCategoryList = ['zh', 'st', 'tt', 'zz', 'qcd', 'zjets']
phyObjList = ['RecDiMuon', 'RecDiJet']
selectKineDict = {'Match': ['Pt', 'Eta', 'Phi', 'M']}
sidebandPath = './sideband'
srPath = './sr'
outputPath = './stack'
checkEnv(args.type, sidebandPath, srPath, outputPath)

histEdgeDict = {'M': {'RecDiMuon': '60, 75, 105', 'RecDiJet': '75, 50, 200'}, 'Pt':'50, 0, 500', 'Eta':'60, -6, 6', 'Phi':'40, -4, 4'}
if args.type == 'mcData': 
    sampleCategoryList.append('data')
elif args.type == 'srSideband':
    sampleCategoryList.append('sumSideband')

for select, kine in selectKineDict.items():
    for k in kine:
        for phyObj in phyObjList:
            for sample in sampleCategoryList:
                if k == 'M':
                    histEdge = histEdgeDict['M'][phyObj]
                else:
                    histEdge = histEdgeDict[k]
                exec('{0}_{1}_{2}_{3} = ROOT.TH1F("{0}_{1}_{2}_{3}", "{0}_{1}_{2}_{3}", {4})'.format(
                        sample, phyObj, select, k, histEdge))

fileList = plotHelper.open_root_files("./sideband")
if args.type == 'srSideband':
    fileList = plotHelper.open_root_files("./sr")
    sidebandFileList = plotHelper.open_root_files("./sideband")

for file in fileList:
    zhTree = file.Get("ZHCandidates")
    if zhTree.GetEntries() == 0: continue
    datasetPrimaryName = plotHelper.get_primary_name(file)
    for phyObj in phyObjList:
        for select, kine in selectKineDict.items():
            for k in kine:
                exec('h_{0}_{1}_{2} = plotConfig.Hist("{2}", "{0}", "{1}", "{3}", zhTree)'.format(
                    phyObj, select, k, datasetPrimaryName))
                exec('htemp = h_{0}_{1}_{2}'.format(phyObj, select, k))
                exec('{3}_{0}_{1}_{2} += h_{0}_{1}_{2}.hist'.format(phyObj,
                     select, k, htemp.mcCategory))

if args.type == 'mcData':
    for phyObj in phyObjList:
        for select, kine in selectKineDict.items():
            for k in kine:
                #exec('plotHelper.plot_hist(qcd_{}_{}_{})'.format(phyObj, select, k))
                exec('plotHelper.plot_ratio("{0}", "{0}_{1}_{2}_{3}", zh_{1}_{2}_{3}, st_{1}_{2}_{3}, tt_{1}_{2}_{3}, zz_{1}_{2}_{3}, qcd_{1}_{2}_{3}, zjets_{1}_{2}_{3}, data_{1}_{2}_{3})'.format(
                    args.type, phyObj, select, k))
elif args.type == 'srSideband':
    for file in sidebandFileList:
        if not zhTree: continue
        zhTree = file.Get("ZHCandidates")
        if zhTree.GetEntries() == 0: continue
        datasetPrimaryName = plotHelper.get_primary_name(file)
        if "DoubleMuon" in datasetPrimaryName: continue
        for phyObj in phyObjList:
            for select, kine in selectKineDict.items():
                for k in kine:
                    exec('h_{0}_{1}_{2} = plotConfig.Hist("{2}", "{0}", "{1}", "{3}", zhTree)'.format(
                    phyObj, select, k, datasetPrimaryName))
                    exec(
                        'sumSideband_{0}_{1}_{2} += h_{0}_{1}_{2}.hist'.format(phyObj, select, k))
    for phyObj in phyObjList:
            for select, kine in selectKineDict.items():
                for k in kine:
                    exec('plotHelper.plot_ratio("{0}", "{0}_{1}_{2}_{3}", zh_{1}_{2}_{3}, st_{1}_{2}_{3}, tt_{1}_{2}_{3}, zz_{1}_{2}_{3}, qcd_{1}_{2}_{3}, zjets_{1}_{2}_{3}, sumSideband_{1}_{2}_{3})'.format(
                        args.type, phyObj, select, k))