import os
import ROOT
import plotHelper
import plotConfig
from array import array

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
sampleCategoryList = ['zh', 'st', 'tt', 'zz', 'qcd', 'zjets', 'sumSideband']
phyObjList = ['RecDiMuon', 'RecDiJet']
selectKineList = ['Match']
sidebandPath = './sideband' # input sideband TTree path
srPath = './sr' # input Signal Region TTree path
outputPath = './stack' # output THStack path
checkEnv("srSideband", sidebandPath, srPath, outputPath)

edgeArray = array('d', [0, 10, 20, 30, 40, 50, 60, 80, 100, 120,
                  140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 500])

for select in selectKineList:
        for phyObj in phyObjList:
            for sample in sampleCategoryList:
                    exec('{0}_{1}_{2}_Pt = ROOT.TH1F("{0}_{1}_{2}_Pt", "{0}_{1}_{2}_Pt", 21, edgeArray)'.format(
                        sample, phyObj, select))

srFileList = plotHelper.open_root_files("./sr")
sbFileList = plotHelper.open_root_files("./sideband")

for sbFile in sbFileList:
	zhTreeSB = sbFile.Get("ZHCandidates")
	if zhTreeSB.GetEntries() == 0: continue
	datasetPrimaryName = plotHelper.get_primary_name(sbFile)
	if "DoubleMuon" in datasetPrimaryName: continue
	for phyObj in phyObjList:
		for select in selectKineList:
			k = 'Pt'
			exec('sb_h_{0}_{1}_{2} = plotConfig.Hist("{2}", "{0}", "{1}", "{3}", zhTreeSB)'.format(phyObj, select, k, datasetPrimaryName))
			exec('plotHelper.check_hist(sb_h_{0}_{1}_{2})'.format(phyObj, select, k))
			exec('sumSideband_{0}_{1}_{2} += sb_h_{0}_{1}_{2}.hist'.format(phyObj, select, k))

for i in sbFileList:
	i.Close()

for srFile in srFileList:
	zhTree = srFile.Get("ZHCandidates")
	if zhTree.GetEntries() == 0: continue
	datasetPrimaryName = plotHelper.get_primary_name(srFile)
	for phyObj in phyObjList:
			for select in selectKineList:
				k = 'Pt'
				exec('h_{0}_{1}_{2} = plotConfig.Hist("{2}", "{0}", "{1}", "{3}", zhTree)'.format(phyObj, select, k, datasetPrimaryName))  # get hist
				exec('htemp = h_{0}_{1}_{2}'.format(phyObj, select, k))
				exec('{3}_{0}_{1}_{2} += htemp.hist'.format(phyObj, select, k, htemp.mcCategory))# category hist


# plot THStack
for phyObj in phyObjList:
	for select in selectKineList:
		k = 'Pt'
		exec('plotHelper.plot_ratio("{0}", "{0}_{1}_{2}_{3}", zh_{1}_{2}_{3}, st_{1}_{2}_{3}, tt_{1}_{2}_{3}, zz_{1}_{2}_{3}, qcd_{1}_{2}_{3}, zjets_{1}_{2}_{3}, sumSideband_{1}_{2}_{3})'.format("srSideband", phyObj, select, k))