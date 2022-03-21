import ROOT

def cal_diff_xs(hist, channel: str):
	nBins = hist.GetNbinsX()
	nEvents = hist.GetEntries()
	if channel == "qqzh":
		lumi = nEvents / (79.24 / 0.100974) # lumi unit: fb^-1 N * BR(Zll) / sigma(ZH)
	elif channel == "ggzh":
		lumi = nEvents / (6.954 / 0.100974)
	else: raise SystemExit("The process of ppZH is wrong!")
	for i in range(1, nBins + 1):
		binWidth = hist.GetBinWidth(i)
		oldBinError = hist.GetBinError(i)
		binDiffXS = hist.GetBinContent(i) * 0.5824 / (lumi * binWidth) # dsigma(ZH) * BR(Hbb)
		hist.SetBinContent(i, binDiffXS)
		newBinError = oldBinError * 0.5824 / (lumi * binWidth)
		hist.SetBinError(i, newBinError)
	print("Total XS for {}: {}".format(channel, hist.Integral("width")))
	return hist

def save_hist(*histList) -> None:
	c = ROOT.TCanvas()
	for hist in histList:
		if "gen" in hist.GetTitle():
			hist.GetXaxis().SetTitle("p_{T} (H)")
			hist.GetYaxis().SetTitle("d #sigma / d p_{T} [fb/GeV]")
			hist.SetTitle("genHiggsXS")
			hist.SetName("genHiggsXS")
			hist.Draw()
			c.SaveAs("genXSPt.pdf")
		if "pfjets" in hist.GetTitle():
			hist.GetXaxis().SetTitle("p_{T} (H)")
			hist.GetYaxis().SetTitle("d #sigma / d p_{T} [fb/ N GeV]")
			hist.SetTitle("recoHiggsXS")
			hist.SetName("recoHiggsXS")
			hist.Draw()
			c.SaveAs("recoXSPt.pdf")
		print("{} Total XS: {} fb".format(hist.GetTitle(), hist.Integral("width")))

def runXS(fileName: str, processType: str):

	f = ROOT.TFile(fileName)
	h_dijet_genparticle_pt = f.Get("demo/h_dijet_genparticle_pt")
	h_dijet_pfjets_pt = f.Get("demo/h_dijet_pfjets_pt")

	genZHXS = cal_diff_xs(h_dijet_genparticle_pt, processType)
	recoZHXS = cal_diff_xs(h_dijet_pfjets_pt, processType)

	genZHXS.SetDirectory(ROOT.gROOT)
	recoZHXS.SetDirectory(ROOT.gROOT)

	return genZHXS, recoZHXS

ROOT.gROOT.SetBatch()

qqZHGen = ROOT.TH1F()
ggZHGen = ROOT.TH1F()
qqZHReco = ROOT.TH1F()
ggZHReco = ROOT.TH1F()

qqZHGen, qqZHReco = runXS("qqZHXS.root", "qqzh")
ggZHGen, ggZHReco = runXS("ggZHXS.root", "ggzh")

genSumXS = qqZHGen + ggZHGen
genSumXS.SetTitle("genSumXS")
recoSumXS = qqZHReco + ggZHReco
recoSumXS.SetTitle("recoSumXS")

fNew = ROOT.TFile("./HiggsXS.root", "recreate")
save_hist(genSumXS, recoSumXS)
qqZHGen.SetName("qqZHGen")
ggZHGen.SetName("ggZHGen")
qqZHGen.Write()
ggZHGen.Write()
genSumXS.Write()
recoSumXS.Write()
fNew.Close()