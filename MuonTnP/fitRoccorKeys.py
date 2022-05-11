import ROOT

ROOT.gROOT.SetBatch(1)

yearList = ["2018", "2017", "2016", "2016APV"]
dataSetTypeList = ["noRoccor", "roccor"]
fitResult = []

for year in yearList:
	for dataSetType in dataSetTypeList:
		print("Start fitting {} {}".format(year, dataSetType))
		fitMassName = "z_mass_no_roccor"
		lineColor = ROOT.kRed
		roccorStatus = "Before"
		if dataSetType == "roccor":
			fitMassName = "z_mass_roccor"
			lineColor = ROOT.kBlue
			roccorStatus = "After"
		f = ROOT.TFile("DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/DYTreeNoBCut{}Skim.root".format(year), "read")
		zhTree = f.Get("dyTree")
		zM = ROOT.RooRealVar(fitMassName, fitMassName, 75, 105)
		ds = ROOT.RooDataSet("ds", "ds", zhTree, ROOT.RooArgSet(zM))
		kest = ROOT.RooKeysPdf("kest", "kest", zM, ds, ROOT.RooKeysPdf.MirrorBoth)

		mass = ROOT.RooRealVar("mass", "mass of Z boson", 0, -5, 5)
		# mass = ROOT.RooRealVar("mass", "mass of Z boson", 90, 85, 95) # only for debugging
		sigma = ROOT.RooRealVar("sigma", "width of Gauss", 0.9, 0.05, 5.0)
		gauss = ROOT.RooGaussian("gauss", "gauss", zM, mass, sigma)
		sig = ROOT.RooFFTConvPdf("sig", "sig", zM, kest, gauss)
		#sig = gauss # only for debugging
		sig.fitTo(ds, ROOT.RooFit.NumCPU(12, 0))

		xFrameCorr = zM.frame()
		ds.plotOn(xFrameCorr, ROOT.RooFit.MarkerStyle(24))
		sig.plotOn(xFrameCorr, ROOT.RooFit.LineColor(lineColor))
		pullHist = xFrameCorr.pullHist()

		cComp = ROOT.TCanvas("cComp", "cComp", 800, 600)
		topPad = ROOT.TPad("topPad", "topPad", 0, 0.3, 1, 1)
		bottomPad = ROOT.TPad("bottomPad", "bottomPad", 0, 0, 1, 0.3)
		cComp.Draw()
		topPad.Draw()
		bottomPad.Draw()
		topPad.cd()
		topPad.SetBottomMargin(0)
		yearMark = ROOT.TLatex()
		yearMark.SetTextFont(42)
		xFrameCorr.SetTitle("")
		xFrameCorr.Draw()
		xFrameCorr.GetYaxis().SetTitle("A.U. / 0.3 GeV")
		xFrameCorr.GetYaxis().SetTitleSize(0.05)
		xFrameCorr.GetYaxis().SetLabelSize(0.05)
		xFrameCorr.GetYaxis().SetTitleOffset(1)
		
		topPad.Update()
		latexLeftPointX = 0.6
		if year == "2016APV":
			latexLeftPointX = 0.55
		yearMark.DrawLatexNDC(latexLeftPointX, 0.92, "{} RoccoR (13 TeV, {})".format(roccorStatus, year))
		bottomPad.cd()
		bottomPad.SetTopMargin(0)
		bottomPad.SetBottomMargin(0.3)
		xFramePull = zM.frame()
		xFramePull.addObject(pullHist, "p")
		xFramePull.SetTitle("")
		pullHist.SetMarkerStyle(24)
		pullHist.SetLineWidth(0)
		xFramePull.GetYaxis().SetTitle("Pull = #frac{MC - Fit}{#sigma_{MC}}")
		xFramePull.GetYaxis().SetTitleSize(0.1)
		xFramePull.GetYaxis().SetLabelSize(0.13)
		xFramePull.GetYaxis().SetNdivisions(505)
		#xFramePull.GetYaxis().SetTickLength(0.01)
		xFramePull.GetYaxis().SetTitleOffset(0.4)
		#xFramePull.GetYaxis().SetLimits(-3.9, 3.9)
		xFramePull.GetXaxis().SetTitle("M_{Z} [GeV]")
		xFramePull.GetXaxis().SetTitleSize(0.13)
		xFramePull.GetXaxis().SetLabelSize(0.13)
		xFramePull.GetXaxis().SetTitleOffset(1.1)
		xFramePull.SetMinimum(pullHist.GetYaxis().GetXmin() * 1.1)
		xFramePull.SetMaximum(pullHist.GetYaxis().GetXmax() * 1.1)
		xFramePull.Draw()
		bottomPad.Update()
		cComp.Update()
		cComp.SaveAs("chap6_{}_{}.pdf".format(dataSetType, year))

		hPdf = sig.createHistogram("hPdf", zM, ROOT.RooFit.Binning(100, 75, 105))
		massFit = hPdf.GetMean()
		massFitErr = hPdf.GetMeanError()
		fitResultPerYear = "{}_{}: mZ = {} +/- {}".format(year, dataSetType, massFit, massFitErr)
		print(fitResultPerYear)
		fitResult += "{}\n".format(fitResultPerYear)

with open("roccorFitResult.txt", 'w') as f:
	f.writelines(fitResult)