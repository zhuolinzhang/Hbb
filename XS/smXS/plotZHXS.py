import ROOT
import json

def get_scale_factor(dataset):
	with open('../../Database/MCInfo2018.json') as mcInfo:
            mcInfoList = json.load(mcInfo)
	factor = 1
	for eachDataset in mcInfoList:
		for value in eachDataset.values():
			if dataset == value:
				factor = eachDataset["factor_IsoMu20"]
				break
	if factor == 1:
		print("Your dataset name is not in the json file!")
	return factor

def cal_diff_xs(hist):
	nBins = hist.GetNbinsX()
	nEvents = hist.GetEntries()
	lumi = nEvents / 79.24
	for i in range(1, nBins + 1):
		binWidth = hist.GetBinWidth(i)
		oldBinError = hist.GetBinError(i)
		binDiffXS = hist.GetBinContent(i) / (lumi * binWidth)
		hist.SetBinContent(i, binDiffXS)
		newBinError = oldBinError / (lumi * binWidth)
		hist.SetBinError(i, newBinError)
	return hist

def save_hist(*histList):
	c = ROOT.TCanvas()
	for hist in histList:
		if "gen" in hist.GetTitle():
			hist.GetXaxis().SetTitle("p_{T}^{Higgs}")
			hist.GetYaxis().SetTitle("d #sigma / d p_{T} [fb/GeV]")
			hist.SetTitle("genHiggsXS")
			hist.SetName("genHiggsXS")
			hist.Draw()
			c.SaveAs("genXSPt.pdf")
		if "pfjets" in hist.GetTitle():
			hist.GetXaxis().SetTitle("p_{T}^{Dijets}")
			hist.GetYaxis().SetTitle("d #sigma / d p_{T} [fb/ N GeV]")
			hist.SetTitle("recoHiggsXS")
			hist.SetName("recoHiggsXS")
			hist.Draw()
			c.SaveAs("recoXSPt.pdf")
		print("{} Total XS: {} fb".format(hist.GetTitle(), hist.Integral("width")))

ROOT.gROOT.SetBatch()
f = ROOT.TFile("./newHiggsHist.root")
h_dijet_genparticle_pt = f.Get("demo/h_dijet_genparticle_pt")
h_dijet_pfjets_pt = f.Get("demo/h_dijet_pfjets_pt")
#h_dijet_genparticle_pt.Scale(get_scale_factor("ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8"))
#h_dijet_pfjets_pt.Scale(get_scale_factor("ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8"))

genZHXS = cal_diff_xs(h_dijet_genparticle_pt)
recoZHXS = cal_diff_xs(h_dijet_pfjets_pt)
save_hist(genZHXS, recoZHXS)

fNew = ROOT.TFile("./HiggsXS.root", "recreate")
genZHXS.Write()
recoZHXS.Write()
fNew.Close()