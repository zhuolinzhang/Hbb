import os
import ROOT
import plotConfig
import plotHelper

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

sampleCategoryList = ['zh', 'st', 'tt', 'zz', 'qcd', 'zjets']
phyObjList = ['RecDiMuon', 'RecDiJet']
selectKineDict = {'Match': ['Pt', 'Eta', 'Phi', 'M']}
sidebandPath = './sideband' # input sideband TTree path
srPath = './sr' # input Signal Region TTree path
outputPath = './stack' # output THStack path

histEdgeDict = {'M': {'RecDiMuon': '60, 75, 105', 'RecDiJet': '75, 50, 200'}, 'Pt':'50, 0, 500', 'Eta':'60, -6, 6', 'Phi':'40, -4, 4'}
sampleCategoryList.append('data')

# generate categorized histograms e.g. zh_RecDiMuon_Match_M
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

# open .root files
fileList = plotHelper.open_root_files("./sideband")

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
                exec('htemp = h_{0}_{1}_{2}'.format(phyObj, select, k))
                exec('{3}_{0}_{1}_{2} += h_{0}_{1}_{2}.hist'.format(phyObj,
                     select, k, htemp.mcCategory))# category hist

    # plot THStack
for phyObj in phyObjList:
    for select, kine in selectKineDict.items():
        for k in kine:
                #exec('plotHelper.plot_hist(qcd_{}_{}_{})'.format(phyObj, select, k)) # just for test
            exec('plotHelper.write_to_root("{0}", "{2}", zh_{0}_{1}_{2}, st_{0}_{1}_{2}, tt_{0}_{1}_{2}, zz_{0}_{1}_{2}, qcd_{0}_{1}_{2}, zjets_{0}_{1}_{2}, data_{0}_{1}_{2})'.format(
                    phyObj, select, k))
