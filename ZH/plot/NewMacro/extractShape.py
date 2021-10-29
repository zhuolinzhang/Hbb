import ROOT
from typing import List
import os
from categorizeTree import readDatabase

def plotHistInEdge(dataframe, branchName: str, scaleFactor: float, binLow: float, binUp: float):
	if binUp != 500:
		hist = dataframe.Filter("higgs_pt >= {} && higgs_pt < {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName)
	else:
		hist = dataframe.Filter("higgs_pt >= {} && higgs_pt <= {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName)
	hist.Scale(scaleFactor)
	hist.Print()
	return hist.Clone()

def extractHistFromTree(category: str, yearList: List[str], sourcePath: str, outputPath: str, binLow: float, binUp: float) -> None:
	print("Categorize {} From {} GeV to {} GeV".format(category, binLow, binUp))
	infoName = "MCInfo"
	if category == "data": infoName = "DataInfo"
	datasetInfoList = []
	
	hHiggsMass = ROOT.TH1D("{}HiggsMass".format(category), "", 75, 50, 200)
	
	for year in set(yearList):
		datasetInfoList += readDatabase("../../../Database/{}{}.json".format(infoName, year), category)
	for dataset in datasetInfoList:
		if not os.path.exists("{}/{}_{}.root".format(sourcePath, dataset["primaryName"], dataset["campaign"])):
			print("{}/{}_{}.root is NOT existed! ".format(sourcePath, dataset["primaryName"], dataset["campaign"]))
			continue
		print("Read {}_{}.root".format(dataset["primaryName"], dataset["campaign"]))
		d = ROOT.RDataFrame("ZHCandidates", "{}/{}_{}.root".format(sourcePath, dataset["primaryName"], dataset["campaign"]))
		if d.Count().GetValue() == 0: continue
		if category == "data": factor = 1
		else: 
			factor = dataset["factor"]
		hHiggsMass += plotHistInEdge(d, "higgs_mass", factor, binLow, binUp) 
	if hHiggsMass.GetEntries() != 0:
		fOut = ROOT.TFile("{}/{}_{}_to_{}.root".format(outputPath, category, binLow, binUp), "recreate")
		hHiggsMass.Write()
		fOut.Close()

def writeShapeFile(sourcePath: str, outputPath: str, binLow: float, binUp: float):
	categoryList = ["zh", "zz", "zjets", "qcd", "tt", "st", "data"]
	fOut = ROOT.TFile("{}/shape_{}_to_{}.root".format(outputPath, binLow, binUp), "recreate")
	fOut.mkdir("ZHbb")
	
	for category in categoryList:
		if category != "data":
				histName = category
		else: histName = "data_obs"
		if os.path.exists("{}/{}_{}_to_{}.root".format(sourcePath, category, binLow, binUp)):
			f = ROOT.TFile("{}/{}_{}_to_{}.root".format(sourcePath, category, binLow, binUp), "read")
			hist = ROOT.TH1F("{}".format(category), "", 75, 50, 200)
			htemp = f.Get("{}HiggsMass".format(category))
			htemp.Copy(hist)
			fOut.cd("ZHbb")
			hist.SetName("{}".format(histName))
			hist.SetTitle("{}".format(histName))
			hist.Write()
			f.Close()
		else:
			hist = ROOT.TH1F("{}".format(histName), "{}".format(histName), 75, 50, 200)
			hist.Write()

	fOut.Close()

def produceDatacard(sourcePath: str, outputPath: str, binLow: float, binUp: float) -> None:
	print("Write Datacard in Bin {} GeV to {} GeV".format(binLow, binUp))
	ptCenter = (binLow + binUp) / 2
	fShape = ROOT.TFile("{}/shape_{}_to_{}.root".format(sourcePath, binLow, binUp), "read")

	
	zhH = fShape.Get("ZHbb/zh")
	zzH = fShape.Get("ZHbb/zz")
	zjetsH = fShape.Get("ZHbb/zjets")
	qcdH = fShape.Get("ZHbb/qcd")
	ttH = fShape.Get("ZHbb/tt")
	stH = fShape.Get("ZHbb/st")
	dataH = fShape.Get("ZHbb/data_obs")
	
	zhN = zhH.Integral()
	zzN = zzH.Integral()
	zjetsN = zjetsH.Integral()
	qcdN = qcdH.Integral()
	ttN = ttH.Integral()
	stN = stH.Integral()
	dataN = dataH.Integral()

	with open("{}/dataCard_mH{}.txt".format(outputPath, ptCenter), 'w') as ftxt:
		ftxt.write("imax    1 number of bins\n")
		ftxt.write("jmax    5 number of processes minus 1\n")
		ftxt.write("kmax    * number of nuisance parameters\n")
		ftxt.write("-" * 50 + "\n")
		ftxt.write("shapes * * shape_{}_to_{}.root ZHbb/$PROCESS ZHbb/$PROCESS_$SYSTEMATIC\n".format(binLow, binUp))
		ftxt.write("-" * 50 + "\n")
		ftxt.write("bin          ZHbb\n")
		ftxt.write("observation  {}\n".format(dataN))
		ftxt.write("-" * 50 + "\n")
		ftxt.write("bin\t\tZHbb\tZHbb\tZHbb\tZHbb\tZHbb\tZHbb\n")
		ftxt.write("process\t\tzh\tzz\tzjets\tqcd\ttt\tst\n")
		ftxt.write("process\t\t0\t1\t2\t3\t4\t5\n")
		ftxt.write("rate\t\t{}\t{}\t{}\t{}\t{}\t{}\n".format(zhN, zzN, zjetsN, qcdN, ttN, stN))
		ftxt.write("-" * 50 + "\n")
		ftxt.write("lumi13TeV_2018\tlnN\t1.023\t1.023\t1.023\t1.023\t1.023\t1.023\n")
		ftxt.write("BR_hbb\tlnN\t1.005\t-\t-\t-\t-\t-\n")
		ftxt.write("pdf_Higgs_qqbar\tlnN\t1.01\t-\t-\t-\t-\t-\n")
		ftxt.write("* autoMCStats 0\n")

def checkFolder(path: str) -> None:
	if os.path.exists(path):
		pass
	else: os.mkdir(path)

edgeList = [0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 500]
categoryList = ["zh", "zz", "zjets", "qcd", "tt", "st", "data"]
checkFolder("histsInEdge")
checkFolder("shapes")
checkFolder("datacards")
'''
for category in categoryList:
	for index, i in enumerate(edgeList):
		if i != 500:
			extractHistFromTree(category, ["2016APV", "2016", "2017", "2018"], "source", "histsInEdge", i, edgeList[index + 1])
		else: break
'''
for index, i in enumerate(edgeList):
		if i != 500:
			writeShapeFile("histsInEdge", "shapes", i, edgeList[index + 1])
			produceDatacard("shapes", "datacards", i, edgeList[index + 1])
		else: break