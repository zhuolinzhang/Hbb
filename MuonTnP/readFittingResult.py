from typing import Dict
import ROOT
import numpy as np
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="The folder which save results")
args = parser.parse_args()

def makeLegend(legend, **hist):
	legend.AddEntry(hist["mc"], "DYJetsToLL 2018", "PL")
	legend.AddEntry(hist["data"], "Data 2018", "PL")

def makeTH1FromTGraph(graph):
	histEdgeArray = np.array([], 'd')
	nPointsGraph = graph.GetN()
	for i in range(0, nPointsGraph):
		binLowEdge = graph.GetPointX(i) - graph.GetErrorXlow(i)
		histEdgeArray = np.append(histEdgeArray, binLowEdge)
		if i == nPointsGraph:
			binUpperEdge = graph.GetPointX(i) + graph.GetErrorXhigh(i)
			histEdgeArray = np.append(histEdgeArray, binUpperEdge)
	hist = ROOT.TH1D("hist", "", nPointsGraph, histEdgeArray)
	for bin in range(1, nPointsGraph + 1):
		hist.SetBinContent(bin, graph.GetPointY(bin - 1))
		hist.SetBinError(bin, max(graph.GetErrorYhigh(bin - 1), graph.GetErrorYlow(bin - 1)))
	return hist

def makeResultDict(ratio: np.array, errors: np.array, ptBinEdge: np.array) -> Dict[str, Dict[str, float]]:
	dictForAbsEta = {}
	for i in range(np.size(ptBinEdge)):
		if i == np.size(ptBinEdge) - 1: break
		dictForAbsEta["pt:[{:d},{:d}]".format(int(ptEdgeArray[i]), int(ptEdgeArray[i + 1]))] = {"stat": 0, "value": 0}
		dictForAbsEta["pt:[{:d},{:d}]".format(int(ptEdgeArray[i]), int(ptEdgeArray[i + 1]))]["stat"] = errors[i]
		dictForAbsEta["pt:[{:d},{:d}]".format(int(ptEdgeArray[i]), int(ptEdgeArray[i + 1]))]["value"] = ratio[i]
		#print(dictForAbsEta)
	return dictForAbsEta

filesDict = {"ID": "tpTree/looseID/fit_eff", "Iso": "tpTree/TightIso_LooseID/fit_eff"}
numDict = {"ID": "LooseID", "Iso": "TightRelIso"}
demDict = {"ID": "TrackerMuons", "Iso": "LooseID"}
#filesDict = {"ID": "tpTree/looseID/fit_eff"}
fileYAxis = {"ID": "Loose ID/Trk.", "Iso": "Tight PFIso/Loose ID", "Trigger": "Trigger/PFIso"}
ptEdgeArray = np.array([15, 20, 25, 30, 40, 50, 60, 120], 'd')
ptNBins = np.size(ptEdgeArray) - 1
etaEdge = [0, 0.9, 1.2, 2.1, 2.4]
absEtaTLatex = ["{} < |#eta| < {}".format(etaEdge[i], etaEdge[i + 1]) for i in range(0, len(etaEdge) - 1)]
binCenterArray = (ptEdgeArray[0:-1] + ptEdgeArray[1:]) / 2
binWidth = np.diff(ptEdgeArray) / 2
for effType, pathName in filesDict.items():
	typeResultDict = {"NUM_{}_DEN_{}".format(numDict[effType], demDict[effType]): {"abseta_pt": {}}}
	for absEtaIndex, absEta in enumerate(etaEdge):
		if absEta == 2.4: break
		print("Read {} in {}<|eta|<{}".format(effType, absEta, etaEdge[absEtaIndex + 1]))
		mcEffArray = np.array([], 'd')
		mcEffUpError = np.array([], 'd')
		mcEffDownError = np.array([], 'd')
		dataEffArray = np.array([], 'd')
		dataEffUpError = np.array([], 'd')
		dataEffDownError = np.array([], 'd')
		for ptBinNum in range(ptNBins):
			print("Read TnP_Muon_{}_{}.root".format(absEtaIndex, ptBinNum))
			mcF = ROOT.TFile("./{}/MC_TnP_Muon_{}_{}_{}.root".format(args.f, effType, absEtaIndex, ptBinNum), "read")
			dataF = ROOT.TFile("./{}/Data_TnP_Muon_{}_{}_{}.root".format(args.f, effType, absEtaIndex, ptBinNum), "read")
			mcResults = mcF.Get(pathName)
			dataResults = dataF.Get(pathName)
			mcEffsResults = mcResults.get(0)
			dataEffsResults = dataResults.get(0)
			mcEff = mcEffsResults.find("efficiency")
			if not mcEff:
				mcEffArray = np.append(mcEffArray, 0)
				mcEffUpError = np.append(mcEffUpError, 0)
				mcEffDownError = np.append(mcEffDownError, 0)
			else:
				mcEffArray = np.append(mcEffArray, mcEff.getVal())
				mcEffUpError = np.append(mcEffUpError, mcEff.getAsymErrorHi())
				mcEffDownError = np.append(mcEffDownError, mcEff.getAsymErrorLo())

			dataEff = dataEffsResults.find("efficiency")
			if not dataEff:
				dataEffArray = np.append(dataEffArray, 0)
				dataEffUpError = np.append(dataEffUpError, 0)
				dataEffDownError = np.append(dataEffDownError, 0)
			else:
				dataEffArray = np.append(dataEffArray, dataEff.getVal())
				dataEffUpError = np.append(dataEffUpError, dataEff.getAsymErrorHi())
				dataEffDownError = np.append(dataEffDownError, dataEff.getAsymErrorLo())
			mcF.Close()
			dataF.Close()
		mcGraph = ROOT.TGraphAsymmErrors(ptNBins, binCenterArray, mcEffArray, binWidth, binWidth, mcEffDownError, mcEffUpError)
		dataGraph = ROOT.TGraphAsymmErrors(ptNBins, binCenterArray, dataEffArray, binWidth, binWidth, dataEffDownError, dataEffUpError)
		mcGraph.SetMarkerStyle(24)
		mcGraph.SetMarkerColor(ROOT.kBlue)
		mcGraph.SetLineColor(ROOT.kBlue)
		dataGraph.SetMarkerStyle(20)

		mcTH1 = makeTH1FromTGraph(mcGraph)
		dataTH1 = makeTH1FromTGraph(dataGraph)
		dataTH1.Divide(mcTH1)
		ratioErrors = np.array([], 'd')
		for bin in range(1, dataTH1.GetNbinsX() + 1):
			ratioErrors = np.append(ratioErrors, dataTH1.GetBinError(bin))

		effMultiGraph = ROOT.TMultiGraph()
		effMultiGraph.Add(mcGraph)
		effMultiGraph.Add(dataGraph)
		effMultiGraph.GetXaxis().SetTitle("Probe Muon p_{T} [GeV]")
		effMultiGraph.GetYaxis().SetTitle("Efficiency {}".format(fileYAxis[effType]))
		effMultiGraph.GetYaxis().SetTitleSize(0.045)
		effMultiGraph.GetYaxis().SetLabelSize(0.045)
		effMultiGraph.GetYaxis().SetRangeUser(0.7, 1.2)
		effMultiGraph.GetXaxis().SetLimits(ptEdgeArray[0], ptEdgeArray[-1])
		effMultiGraph.SetTitle("")

		absEtaBinLatex = ROOT.TLatex()
		cmsTag = ROOT.TLatex()
		statusTag = ROOT.TLatex()
		
		ratioEffArray = dataEffArray / mcEffArray
		ratioGraph = ROOT.TGraphErrors(ptNBins, binCenterArray, ratioEffArray, binWidth, ratioErrors)
		ratioGraph.SetTitle("")
		ratioGraph.GetXaxis().SetLimits(ptEdgeArray[0], ptEdgeArray[-1])
		ratioGraph.GetXaxis().SetLabelSize(0.14)
		ratioGraph.GetXaxis().SetTitleSize(0.14)
		ratioGraph.GetXaxis().SetTitle("Probe Muon p_{T} [GeV]")
		ratioGraph.GetYaxis().SetRangeUser(0.8, 1.2)
		ratioGraph.GetYaxis().SetTitle("Data/MC")
		ratioGraph.GetYaxis().SetLabelSize(0.13)
		ratioGraph.GetYaxis().SetTitleSize(0.13)
		ratioGraph.GetYaxis().SetTitleOffset(0.4)
		ratioGraph.GetYaxis().SetNdivisions(505)
		ratioGraph.SetMarkerStyle(20)
		leg = ROOT.TLegend(0.64, 0.7, 0.9, 0.9)
		leg.SetTextSize(0.05)
		#leg.AddEntry(mcGraph, "DYJetsToLL 2018", "PL")
		#leg.AddEntry(dataGraph, "Data 2018", "PL")
		makeLegend(leg, mc=mcGraph, data=dataGraph)
		c = ROOT.TCanvas("c", "", 800, 600)
		upperPad = ROOT.TPad("upperPad", "upperPad", 0., 0.3, 1. , 1.)
		lowerPad = ROOT.TPad("lowerPad", "lowerPad", 0., 0., 1. , 0.3)
		upperPad.Draw()
		lowerPad.Draw()
		upperPad.SetTicks(1, 1)
		upperPad.SetBottomMargin(0.)
		upperPad.cd() # active uppper pad
		effMultiGraph.Draw("ap")
		absEtaBinLatex.DrawLatexNDC(0.13, 0.73, "#scale[0.8]{{{}}}".format(absEtaTLatex[absEtaIndex]))
		cmsTag.DrawLatexNDC(0.13, 0.83, "#scale[1.2]{CMS}")
		statusTag.DrawLatexNDC(0.13, 0.78, "#font[52]{Work in Progress}")
		leg.Draw("same")
		lowerPad.cd()
		lowerPad.SetTopMargin(0.)
		lowerPad.SetTicks(1, 1)
		lowerPad.SetGridy()
		lowerPad.SetBottomMargin(0.4)
		ratioGraph.Draw("ap")
		c.SaveAs("ratio_{}_{}.pdf".format(effType, absEtaIndex))
		del(leg) # I don't understand the reason, but it makes the script work
		typeResultDict["NUM_{}_DEN_{}".format(numDict[effType], demDict[effType])]["abseta_pt"]["abseta:[{:.1f},{:.1f}]".format(absEta, etaEdge[absEtaIndex + 1])] = makeResultDict(ratioEffArray, ratioErrors, ptEdgeArray)
	typeResultDict["NUM_{}_DEN_{}".format(numDict[effType], demDict[effType])]["abseta_pt"]["binning"] = []
	typeResultDict["NUM_{}_DEN_{}".format(numDict[effType], demDict[effType])]["abseta_pt"]["binning"].append({"binning": list(etaEdge), "variable": "abseta"})
	typeResultDict["NUM_{}_DEN_{}".format(numDict[effType], demDict[effType])]["abseta_pt"]["binning"].append({"binning": list(ptEdgeArray), "variable": "pt"})
	with open("result_{}.json".format(effType), 'w') as f:
		json.dump(typeResultDict, f, indent=4)
