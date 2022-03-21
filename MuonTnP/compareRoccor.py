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

fileList = glob.glob("DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/*.root")

for file in fileList:
	f = ROOT.TFile(file, "read")
	fileName = file.split('/')[-1].rstrip(".root")
	histCorr = ROOT.TH1F()
	histNoCorr = ROOT.TH1F()
	histCorr = f.Get("demo/hZRoccor")
	histNoCorr = f.Get("demo/hZNoRoccor")
	c = ROOT.TCanvas()
	c.Draw()
	histCorr.GetXaxis().SetTitle("m_{Z} [GeV]")
	histCorr.GetYaxis().SetTitle("A.U.")
	histCorr.SetTitle("")
	histCorr.SetLineColor(ROOT.kRed)
	histCorr.SetStats(0)
	hRatio = ROOT.TRatioPlot(histCorr, histNoCorr)
	hRatio.Draw()
	hRatio.SetSeparationMargin(0)
	hRatio.GetLowerRefGraph().GetYaxis().SetTitle("#frac{RoccoR}{No RoccoR}")
	leg = ROOT.TLegend(0.65, 0.7, 0.85, 0.9)
	leg.AddEntry(histCorr, "After RoccoR", 'l')
	leg.AddEntry(histNoCorr, "No RoccoR", 'l')
	leg.SetBorderSize(0)
	leg.Draw()
	year = ROOT.TLatex()
	year.SetTextSize(0.03)
	year.SetTextFont(42)
	year.DrawLatexNDC(0.75, 0.94, "(13 TeV, {})".format(giveYear(fileName)))
	c.SaveAs("DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/chap6_{}.pdf".format(fileName))