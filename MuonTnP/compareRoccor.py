import ROOT
import glob

def giveYear(name: str) -> str:
	if "2016APV" in name:
		return "2016APV"
	elif "2016" in name:
		return "2016"
	elif "2017" in name:
		return "2017"
	elif "2018" in name:
		return "2018"
	else:
		raise SystemExit("No year info in the name of file!")

fileList = glob.glob("DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/DYTreeNoBCut*Skim.root")

for file in fileList:
	f = ROOT.TFile(file, "read")
	fileName = file.split('/')[-1].rstrip(".root")
	histCorr = ROOT.TH1D()
	histNoCorr = ROOT.TH1D()
	#histCorr = f.Get("demo/hZRoccor")
	#histNoCorr = f.Get("demo/hZNoRoccor")
	dyTree = f.Get("dyTree")
	dyTree.Draw("z_mass_no_roccor >> histNoCorr(60, 75, 105)")
	dyTree.Draw("z_mass_roccor >> histCorr(60, 75, 105)")
	histCorr = ROOT.gROOT.FindObject("histCorr")
	histNoCorr = ROOT.gROOT.FindObject("histNoCorr")
	c = ROOT.TCanvas()
	c.Draw()
	histCorr.GetXaxis().SetTitle("m_{Z} [GeV]")
	histCorr.GetYaxis().SetTitle("A.U. / 0.5 GeV")
	histCorr.GetYaxis().SetLabelSize(0.04)
	histCorr.GetYaxis().SetTitleSize(0.04)
	histCorr.GetYaxis().SetTitleOffset(1.4)
	histCorr.SetTitle("")
	histCorr.SetLineColor(ROOT.kRed)
	histCorr.SetStats(0)
	hRatio = ROOT.TRatioPlot(histCorr, histNoCorr)
	hRatio.Draw()
	hRatio.SetSeparationMargin(0)
	hRatio.GetLowerRefGraph().GetYaxis().SetTitle("#frac{RoccoR}{No RoccoR}")
	hRatio.GetLowerRefGraph().GetXaxis().SetLabelSize(0.04)
	hRatio.GetLowerRefGraph().GetXaxis().SetTitleSize(0.04)
	leg = ROOT.TLegend(0.65, 0.7, 0.85, 0.9)
	leg.AddEntry(histCorr, "After RoccoR", 'l')
	leg.AddEntry(histNoCorr, "No RoccoR", 'l')
	leg.SetTextSize(0.04)
	leg.SetBorderSize(0)
	leg.Draw()
	year = ROOT.TLatex()
	year.SetTextSize(0.04)
	year.SetTextFont(42)
	yearXPosition = 0.75
	yearName = giveYear(fileName)
	if yearName == '2016APV':
		yearXPosition -= 0.05
	year.DrawLatexNDC(yearXPosition, 0.94, "(13 TeV, {})".format(yearName))
	c.SaveAs("DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/chap6_{}.pdf".format(fileName))