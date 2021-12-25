import json
from typing import Tuple
import ROOT
import numpy as np

def readSF(path: str) -> Tuple[np.array, np.array]:
	result = {}
	with open(path, 'r') as f:
		result = json.load(f)
	valueArrayShape = [0, 0]
	for binningName in result.values():
		for resultContent in binningName.values():
			valueArrayShape[0] = len(resultContent) - 1
			for ptBinContent in resultContent.values():
				if len(ptBinContent) == 2: break
				valueArrayShape[1] = len(ptBinContent)
	valueArray = np.zeros(valueArrayShape, 'd')
	errorArray = np.zeros(valueArrayShape, 'd')
	for binningName in result.values():
		etaIndex = 0
		for resultContent in binningName.values():
			for absEtaBin, ptResultContent in resultContent.items():
				if absEtaBin == "binning": break
				ptSFIndex = 0
				for sfContent in ptResultContent.values():
					valueArray[etaIndex][ptSFIndex] = sfContent["value"]
					errorArray[etaIndex][ptSFIndex] = sfContent["stat"]
					ptSFIndex += 1
				etaIndex += 1
	return valueArray, errorArray

def readBinningInfo(path: str) -> Tuple:
	result = {}
	sfName = ''
	absetaArray = np.array([], 'd')
	ptArray = np.array([], 'd')
	with open(path, 'r') as f:
		result = json.load(f)
	for sfType, binningName in result.items():
		sfName = sfType
		for resultContent in binningName.values():
			for binningEdge in resultContent["binning"]:
				if binningEdge["variable"] == "abseta":
					absetaArray = np.append(absetaArray, binningEdge["binning"])
				if binningEdge["variable"] == "pt":
					ptArray = np.append(ptArray, binningEdge["binning"])
	return sfName, absetaArray, ptArray

def makeSFTH2(path: str) -> None:
	sf, errors = readSF(path)
	sfName, absEtaBins, ptBins = readBinningInfo(path)
	sfHist = ROOT.TH2D("sf", "", np.size(absEtaBins) - 1, absEtaBins, np.size(ptBins) - 1, ptBins)
	for binX in range(1, sfHist.GetNbinsX() + 1):
		arrayX = binX - 1
		for binY in range(1, sfHist.GetNbinsY() + 1):
			arrayY = binY - 1
			sfHist.SetBinContent(binX, binY, sf[arrayX][arrayY])
			sfHist.SetBinError(binX, binY, errors[arrayX][arrayY])
	c = ROOT.TCanvas()
	sfHist.SetStats(0)
	sfHist.Draw("TEXT COLZ")
	sfHist.GetXaxis().SetTitle("Probe Muon |#eta|")
	sfHist.GetYaxis().SetTitle("Probe Muon p_{T}")
	numName = sfName.split('_')[1]
	denName = sfName.split('_')[3]
	c.SaveAs("./ratio_th2_{}_{}.pdf".format(numName, denName))

makeSFTH2("./result_ID.json")
makeSFTH2("./result_Iso.json")