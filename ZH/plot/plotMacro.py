import os
import ROOT
import plotConfig
import plotHelper
import argparse
from array import array

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", type=str, help="mcData or srSideband The type of THStack")
parser.add_argument("-w", action='store_true', help="write mcData histograms to root file")
args = parser.parse_args()

def checkEnv(stackType, sidebandDataset, SRDataset, output):
    # Check the input files exist. Generate the output folder if it does not exist.
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

ROOT.gROOT.SetBatch(True)
sampleCategoryList = ['zh', 'st', 'tt', 'zz', 'qcd', 'zjets']
phyObjList = ['RecDiMuon', 'RecDiJet']
selectKineDict = {'Match': ['Pt', 'Eta', 'Phi', 'M']}
sidebandPath = './sideband' # input sideband TTree path
srPath = './sr' # input Signal Region TTree path
outputPath = './stack' # output THStack path
checkEnv(args.type, sidebandPath, srPath, outputPath)

histEdgeDict = {'M': {'RecDiMuon': '60, 75, 105', 'RecDiJet': '75, 50, 200'}, 'Eta':'60, -6, 6', 'Phi':'40, -4, 4'}
edgeArray = array('d', [0, 10, 20, 30, 40, 50, 60, 80, 100, 120,
                  140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 500])
if args.type == 'mcData': 
    sampleCategoryList.append('data')
elif args.type == 'srSideband':
    sampleCategoryList.append('sumSideband')

# generate categorized histograms e.g. zh_RecDiMuon_Match_M
for select, kine in selectKineDict.items():
    for k in kine:
        for phyObj in phyObjList:
            for sample in sampleCategoryList:
                if k != 'Pt':
                    if k == 'M':
                        histEdge = histEdgeDict['M'][phyObj]
                    else:
                        histEdge = histEdgeDict[k]
                    exec('{0}_{1}_{2}_{3} = ROOT.TH1F("{0}_{1}_{2}_{3}", "{0}_{1}_{2}_{3}", {4})'.format(
                        sample, phyObj, select, k, histEdge))
                elif k == "Pt":
                    exec('{0}_{1}_{2}_{3} = ROOT.TH1F("{0}_{1}_{2}_{3}", "{0}_{1}_{2}_{3}", 21, edgeArray)'.format(
                        sample, phyObj, select, k))



# open .root files
if args.type == 'mcData':
    fileList = plotHelper.open_root_files("./sideband")
elif args.type == 'srSideband':
    fileList = plotHelper.open_root_files("./sr")
    sidebandFileList = plotHelper.open_root_files("./sideband")

# loop .root files, get the TH1 hist from TTree, category hists
for file in fileList:
    zhTree = file.Get("ZHCandidates")
    if zhTree.GetEntries() == 0: continue
    datasetPrimaryName = plotHelper.get_primary_name(file)
    for phyObj in phyObjList:
        for select, kine in selectKineDict.items():
            for k in kine:
                exec('h_{0}_{1}_{2} = plotConfig.Hist("{2}", "{0}", "{1}", "{3}", zhTree)'.format(
                    phyObj, select, k, datasetPrimaryName)) # get hist
                #if k == 'Pt': exec('plotHelper.check_hist(h_{0}_{1}_{2})'.format(phyObj, select, k))
                exec('htemp = h_{0}_{1}_{2}'.format(phyObj, select, k))
                exec('{3}_{0}_{1}_{2} += h_{0}_{1}_{2}.hist'.format(phyObj,
                     select, k, htemp.mcCategory))# category hist

for i in fileList:
    i.Close()

if args.type == 'mcData':
    # plot THStack
    for phyObj in phyObjList:
        for select, kine in selectKineDict.items():
            for k in kine:
                #exec('plotHelper.plot_hist(zh_{}_{}_{})'.format(phyObj, select, k)) # just for test
                exec('plotHelper.plot_ratio("{0}", "{0}_{1}_{2}_{3}", zh_{1}_{2}_{3}, st_{1}_{2}_{3}, tt_{1}_{2}_{3}, zz_{1}_{2}_{3}, qcd_{1}_{2}_{3}, zjets_{1}_{2}_{3}, data_{1}_{2}_{3})'.format(
                    args.type, phyObj, select, k))
                if args.w:
                    exec('plotHelper.write_to_root("{0}", "{2}", zh_{0}_{1}_{2}, st_{0}_{1}_{2}, tt_{0}_{1}_{2}, zz_{0}_{1}_{2}, qcd_{0}_{1}_{2}, zjets_{0}_{1}_{2}, data_{0}_{1}_{2})'.format(
                    phyObj, select, k)) # this function leads to TH1::Merge
elif args.type == 'srSideband':
    # sum up all sideband hists to the sumSideband_x_x_x hist

    for sbFile in sidebandFileList:
        zhTreeSB = sbFile.Get("ZHCandidates")
        if zhTreeSB.GetEntries() == 0: continue
        datasetPrimaryName = plotHelper.get_primary_name(sbFile)
        if "DoubleMuon" in datasetPrimaryName: continue
        for phyObj in phyObjList:
            for select, kine in selectKineDict.items():
                for k in kine:
                    exec('sb_h_{0}_{1}_{2} = plotConfig.Hist("{2}", "{0}", "{1}", "{3}", zhTreeSB)'.format(phyObj, select, k, datasetPrimaryName))
                    #if k == 'Pt': exec('plotHelper.check_hist(sb_h_{0}_{1}_{2})'.format(phyObj, select, k))
                    exec('sumSideband_{0}_{1}_{2} += sb_h_{0}_{1}_{2}.hist'.format(phyObj, select, k))
    
    for sbFile in sidebandFileList:
        sbFile.Close()

    # plot THStack
    for phyObj in phyObjList:
            for select, kine in selectKineDict.items():
                for k in kine:
                    exec('plotHelper.plot_ratio("{0}", "{0}_{1}_{2}_{3}", zh_{1}_{2}_{3}, st_{1}_{2}_{3}, tt_{1}_{2}_{3}, zz_{1}_{2}_{3}, qcd_{1}_{2}_{3}, zjets_{1}_{2}_{3}, sumSideband_{1}_{2}_{3})'.format(
                        args.type, phyObj, select, k))
