import ROOT
import argparse
import json
from typing import List
from array import array
import os

def readDatabase(jsonPath: str, category: str) -> List[dict]:
	jsonList = []
	datasetList = []
	with open(jsonPath, 'r') as f:
		jsonList = json.load(f)
	for dataset in jsonList:
		if category == dataset["category"]:
			datasetList.append(dataset)
	return datasetList

def categoryH(categoryHist, categoryList: List[dict], sourcePath: str) -> None:
	category, phyObj, kinematic = categoryHist.GetName().split('_')
	for dataset in categoryList:
		if dataset["category"] == category:
			f = ROOT.TFile("{}/{}_{}.root".format(sourcePath, dataset["primaryName"], dataset["campagin"]), "read")
			tree = f.Get("ZHCandidates")
			histRange = ''
			if kinematic == "mass":
				if phyObj == 'z': histRange = "30, 75, 105"
				if phyObj == "higgs": histRange = "75, 50, 200"
			if kinematic == "pt": histRange = "50, 0, 500"
			if kinematic == "eta": histRange = "60, -6, 6"
			if kinematic == "phi": histRange = "40, -4, 4"
			tree.Draw("{0}_{1} >> h_{0}_{1}({2})".format(phyObj, kinematic, histRange))
			h = ROOT.gROOT.FindObject("h_{}_{}".format(phyObj, kinematic))
			h.Scale(dataset["factor"])
			if kinematic == "pt":
				edgeArray = array('d', [0, 10, 20, 30, 40, 50, 60, 80, 100, 120,
                              	140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 500])
				h.Rebin(21, "h_{}_{}".format(phyObj, kinematic), edgeArray)
			categoryHist += h

def plotHistFromRDF(dataframe, branchName: str, scaleFactor: float):
	edgeArray = array('d', [0, 10, 20, 30, 40, 50, 60, 80, 100, 120,
	                  140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 500])
	if "mass" in branchName:
		if "higgs" in branchName:
			hist = dataframe.Histo1D(ROOT.RDF.TH1DModel("", "", 75, 50, 200), branchName)
		if "z" in branchName:
			hist = dataframe.Histo1D(ROOT.RDF.TH1DModel("", "", 60, 75, 105), branchName)
	elif "pt" in branchName:
		hist = dataframe.Histo1D(ROOT.RDF.TH1DModel("", "", 21, edgeArray), branchName)
	elif "eta" in branchName:
		hist = dataframe.Histo1D(ROOT.RDF.TH1DModel("", "", 60, -6, 6), branchName)
	elif "phi" in branchName:
		hist = dataframe.Histo1D(ROOT.RDF.TH1DModel("", "", 40, -4, 4), branchName)
	if scaleFactor != 1: hist.Scale(scaleFactor)
	return hist.Clone()
	
def categoryHistFromTree(category: str, campaignList: List[str], kinematicList: List[str], sourcePath: str, outputPath: str) -> None:
	print("Categorize {}".format(category))
	infoName = "MCInfo"
	if category == "data": infoName = "DataInfo"
	datasetInfoList = []
	yearList = []
	edgeArray = array('d', [0, 10, 20, 30, 40, 50, 60, 80, 100, 120,
	                  140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 500])
	hZMass = ROOT.TH1D("{}ZMass".format(category), "", 60, 75, 105)
	hZPt = ROOT.TH1D("{}ZPt".format(category), "", 21, edgeArray)
	hZEta = ROOT.TH1D("{}ZEta".format(category), "", 60, -6, 6)
	hZPhi = ROOT.TH1D("{}ZPhi".format(category), "", 40, -4, 4)
	hHiggsMass = ROOT.TH1D("{}HiggsMass".format(category), "", 75, 50, 200)
	hHiggsPt = ROOT.TH1D("{}HiggsPt".format(category), "", 21, edgeArray)
	hHiggsEta = ROOT.TH1D("{}HiggsEta".format(category), "", 60, -6, 6)
	hHiggsPhi = ROOT.TH1D("{}HiggsPhi".format(category), "", 40, -4, 4)
	for campaign in campaignList:
		year = campaign.rstrip("UL").rstrip("ReReco")
		yearList.append(year)
	for year in set(yearList):
		datasetInfoList += readDatabase("/Users/zhangzhuolin/Hbb/Database/{}{}.json".format(infoName, year), category)
	for dataset in datasetInfoList:
		if not os.path.exists("{}/{}_{}.root".format(sourcePath, dataset["primaryName"], dataset["campaign"])):
			print("{}/{}_{}.root is NOT existed! ".format(sourcePath, dataset["primaryName"], dataset["campaign"]))
			continue
		d = ROOT.RDataFrame("ZHCandidates", "{}/{}_{}.root".format(sourcePath, dataset["primaryName"], dataset["campaign"]))
		if d.Count().GetValue() == 0: continue
		for kinematic in kinematicList:
			if category == "data": factor = 1
			else: factor = dataset["factorIsoMu20"]
			if kinematic == "mass":
				hZMass += plotHistFromRDF(d, "z_mass", factor)
				hHiggsMass += plotHistFromRDF(d, "higgs_mass", factor) 
			if kinematic == "pt":
				hZPt += plotHistFromRDF(d, "z_pt", factor) 
				hHiggsPt += plotHistFromRDF(d, "higgs_pt", factor) 
			if kinematic == "eta":
				hZEta += plotHistFromRDF(d, "z_eta", factor) 
				hHiggsEta += plotHistFromRDF(d, "higgs_eta", factor) 
			if kinematic == "phi":
				hZPhi += plotHistFromRDF(d, "z_phi", factor) 
				hHiggsPhi += plotHistFromRDF(d, "higgs_phi", factor) 
	histDict = {"hZMass": hZMass, "hZPt": hZPt, "hZEta": hZEta, "hZPhi": hZPhi, "hHiggsMass": hHiggsMass, "hHiggsPt": hHiggsPt, "hHiggsEta": hHiggsEta, "hHiggsPhi": hHiggsPhi}
	fOut = ROOT.TFile("{}/{}.root".format(outputPath, category), "recreate")
	for hist in histDict.values():
		if hist.GetEntries() != 0:
			print(hist.GetName(), hist.GetEntries())
			hist.Write()
	fOut.Close()
