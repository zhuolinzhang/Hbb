import ROOT
from typing import List
import os
from categorizeTree import readDatabase
import json

def plotHistInEdge(dataframe, branchName: str, scaleFactor: float, binLow: float, binUp: float, histType: str):
	'''
		Plot the invariant mass spectrum from the branch in the TTree by RDataFrame
	'''
	if binUp != 600:
		if histType == "nominal":
			hist = dataframe.Filter("higgs_pt >= {} && higgs_pt < {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName, "z_sf")
		elif histType == "data":
			hist = dataframe.Filter("higgs_pt >= {} && higgs_pt < {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName)
		elif histType == "up":
			hist = dataframe.Filter("higgs_pt >= {} && higgs_pt < {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName, "z_sf_up")
		elif histType == "down":
			hist = dataframe.Filter("higgs_pt >= {} && higgs_pt < {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName, "z_sf_down")
	else:
		if histType == "nominal":
			hist = dataframe.Filter("higgs_pt >= {} && higgs_pt <= {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName, "z_sf")
		elif histType == "data":
			hist = dataframe.Filter("higgs_pt >= {} && higgs_pt < {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName)
		elif histType == "up":
			hist = dataframe.Filter("higgs_pt >= {} && higgs_pt <= {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName, "z_sf_up")
		elif histType == "down":
			hist = dataframe.Filter("higgs_pt >= {} && higgs_pt <= {}".format(binLow, binUp)).Histo1D(ROOT.RDF.TH1DModel("hHiggsMass", "", 75, 50, 200), branchName, "z_sf_down")
	hist.Scale(scaleFactor)
	hist.Print()
	return hist.Clone()

def extractHistFromTree(category: str, yearList: List[str], sourcePath: str, outputPath: str, binLow: float, binUp: float) -> None:
	print("-" * 60)
	print("Categorize {} From {} GeV to {} GeV".format(category, binLow, binUp))
	infoName = "MCInfo"
	if category == "data": infoName = "DataInfo"
	datasetInfoList = []
	
	hHiggsMass = ROOT.TH1D("{}HiggsMass".format(category), "", 75, 50, 200)
	hHiggsMassUp = ROOT.TH1D("{}MuonTnpUp".format(category), "", 75, 50, 200)
	hHiggsMassDown = ROOT.TH1D("{}MuonTnpDown".format(category), "", 75, 50, 200)
	
	for year in set(yearList):
		datasetInfoList += readDatabase("/Users/zhangzhuolin/Hbb/Database/{}{}.json".format(infoName, year), category)
	for dataset in datasetInfoList:
		if not os.path.exists("{}/{}_{}.root".format(sourcePath, dataset["primaryName"], dataset["campaign"])):
			print("{}/{}_{}.root is NOT existed! ".format(sourcePath, dataset["primaryName"], dataset["campaign"]))
			continue
		print("Read {}_{}.root".format(dataset["primaryName"], dataset["campaign"]))
		d = ROOT.RDataFrame("ZHCandidates", "{}/{}_{}.root".format(sourcePath, dataset["primaryName"], dataset["campaign"]))
		if d.Count().GetValue() == 0: continue
		if category == "data": 
			factor = 1
			print("Get TH1 from {}_{}.root".format(dataset["primaryName"], dataset["campaign"]))
			hHiggsMass += plotHistInEdge(d, "higgs_mass", factor, binLow, binUp, "data")
		else:
			factor = dataset["factor"]
			print("Get TH1 from {}_{}.root".format(dataset["primaryName"], dataset["campaign"]))
			hHiggsMass += plotHistInEdge(d, "higgs_mass", factor, binLow, binUp, "nominal")
			hHiggsMassUp += plotHistInEdge(d, "higgs_mass", factor, binLow, binUp, "up")
			hHiggsMassDown += plotHistInEdge(d, "higgs_mass", factor, binLow, binUp, "down")

	if hHiggsMass.GetEntries() != 0:
		fOut = ROOT.TFile("{}/{}_{}_to_{}.root".format(outputPath, category, binLow, binUp), "recreate")
		hHiggsMass.Write()
		if category != "data": 
			hHiggsMassUp.Write()
			hHiggsMassDown.Write()
		fOut.Close()
	print("-" * 60)

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
			if category != "data":
				histUp = ROOT.TH1F("{}_muon_tnpUP".format(category), "", 75, 50, 200)
				htempUp = f.Get("{}MuonTnpUp".format(category))
				htempUp.Copy(histUp)
				histUp.SetName("{}_muon_tnpUp".format(category))
				histUp.SetTitle("{}_muon_tnpUp".format(category))
				histDown = ROOT.TH1F("{}_muon_tnpDown".format(category), "", 75, 50, 200)
				htempDown = f.Get("{}MuonTnpDown".format(category))
				htempDown.Copy(histDown)
				histDown.SetName("{}_muon_tnpDown".format(category))
				histDown.SetTitle("{}_muon_tnpDown".format(category))
				fOut.cd("ZHbb")
				histUp.Write()
				histDown.Write()
			fOut.cd("ZHbb")
			hist.SetName("{}".format(histName))
			hist.SetTitle("{}".format(histName))
			hist.Write()
			f.Close()
		else:
			hist = ROOT.TH1F("{}".format(histName), "{}".format(histName), 75, 50, 200)
			histUp = ROOT.TH1F("{}_muon_tnpUp".format(histName), "{}".format(histName), 75, 50, 200)
			histDown = ROOT.TH1F("{}_muon_tnpDown".format(histName), "{}".format(histName), 75, 50, 200)
			hist.Write()
			histUp.Write()
			histDown.Write()

	fOut.Close()

def readNuisanceParas(npPath: str, processList: List[str]) -> List[str]:
	npDict = {}
	npList = []
	with open(npPath, 'r') as f:
		npDict = json.load(f)
	for paraName, paraInfo in npDict.items():
		for process in processList:
			if process in paraInfo:
				pass
			else: paraInfo[process] = '-'
		newLine = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(paraName, paraInfo["type"], paraInfo["zh"], paraInfo["zz"], paraInfo["zjets"], paraInfo["qcd"], paraInfo["tt"], paraInfo["st"])
		npList.append(newLine)
	return npList

def produceDatacard(sourcePath: str, outputPath: str, binLow: float, binUp: float, nuisanceParaPath: str) -> None:
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

	nuisanceParaList = readNuisanceParas(nuisanceParaPath, ["zh", "zz", "zjets", "qcd", "tt", "st"])

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
		for line in nuisanceParaList:
			ftxt.write(line)
		ftxt.write("* autoMCStats 0\n")

def checkFolder(path: str) -> None:
	if os.path.exists(path):
		pass
	else: os.mkdir(path)

#edgeList = [0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 500]
edgeList = [0, 45, 80, 120, 200, 350, 450, 600]
categoryList = ["zh", "zz", "zjets", "qcd", "tt", "st", "data"]
yearList = ["2016APV", "2016", "2017", "2018"]
folderList = ["histsInEdge", "shapes", "datacards"]
for year in yearList:
	for folderName in folderList:
		checkFolder("{}{}".format(folderName, year))
'''
checkFolder("histsInEdge")
checkFolder("shapes")
checkFolder("datacards")
'''

for category in categoryList:
	for index, i in enumerate(edgeList):
		if i != 600:
			#extractHistFromTree(category, ["2016APV", "2016", "2017", "2018"], "source", "histsInEdge", i, edgeList[index + 1])
			#extractHistFromTree(category, ["2016APV"], "source", "histsInEdge", i, edgeList[index + 1])
			for year in yearList:
				extractHistFromTree(category, [year], "source", "histsInEdge{}".format(year), i, edgeList[index + 1])
		else: break

for index, i in enumerate(edgeList):
		if i != 600:
			for year in yearList:
				print("Era {}".format(year))
				writeShapeFile("histsInEdge{}".format(year), "shapes{}".format(year), i, edgeList[index + 1])
				produceDatacard("shapes{}".format(year), "datacards{}".format(year), i, edgeList[index + 1], "./nuisancePara.json")
		else: break
