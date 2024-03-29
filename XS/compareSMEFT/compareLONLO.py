import ROOT

ROOT.gROOT.SetBatch()
fAOD = ROOT.TFile("../smXS/HiggsXS.root")
fLO = ROOT.TFile("./mg5XS_ZH_HToBB_ZToLL_LO.root")
fMG5EFTcpucpBBLO = ROOT.TFile("./mg5XS_ZH_HToBB_ZToLL_SMEFTatLO_cpu_cpBB.root")
fMG5EFTcpucpBBNLO = ROOT.TFile("./mg5XS_ZH_HToBB_ZToLL_SMEFTatNLO_cpu_cpBB.root")
fMG5EFT111LO = ROOT.TFile("./mg5XS_ZH_HToBB_ZToLL_SMEFTatLO_cpW_cpWB_cpq3i.root")
fMG5EFT111NLO = ROOT.TFile("./mg5XS_ZH_HToBB_ZToLL_SMEFTatNLO_cpW_cpWB_cpq3i.root")

hLO = fLO.Get("mg5HiggsXSPt")
hNLO = fAOD.Get("qqZHGen")
hMG5EFTcpucpBBLO = fMG5EFTcpucpBBLO.Get("mg5HiggsXSPt")
hMG5EFTcpucpBBNLO = fMG5EFTcpucpBBNLO.Get("mg5HiggsXSPt")
hMG5EFT111LO = fMG5EFT111LO.Get("mg5HiggsXSPt")
hMG5EFT111NLO = fMG5EFT111NLO.Get("mg5HiggsXSPt")

hNLO.SetTitle("")
hNLO.Scale(0.100974) # hNLO is xs(ZH) times BR(Hbb)
hNLO.GetYaxis().SetTitle("d#sigma(ZH, Z#rightarrow l^{+}l^{-}, H#rightarrow b#bar{b}) / dp_{T} [fb/N GeV]")
hNLO.GetYaxis().SetTitleSize(0.05)
hNLO.GetYaxis().SetLabelSize(0.055)
#hNLO.SetMaximum(9e2)
hNLO.GetYaxis().SetRangeUser(0, 0.5)
hNLO.GetYaxis().SetTitleOffset(0.8)
hNLO.SetStats(0)
hNLO.SetMarkerStyle(32)
hNLO.SetLineColor(ROOT.kRed)
hNLO.SetLineStyle(2)
hNLO.SetMarkerColor(ROOT.kRed)

hLO.SetStats(0)
hLO.SetMarkerStyle(23)
hLO.SetLineColor(ROOT.kRed)
hLO.SetLineStyle(1)
hLO.SetMarkerColor(ROOT.kRed)

hMG5EFT111NLO.SetStats(0)
hMG5EFT111NLO.SetMarkerStyle(28)
hMG5EFT111NLO.SetMarkerColor(ROOT.kBlack)
hMG5EFT111NLO.SetLineColor(ROOT.kBlack)
hMG5EFT111NLO.SetLineStyle(2)
#hMG5EFT111NLO.GetYaxis().SetRangeUser(0, 1.5)
hMG5EFT111LO.SetStats(0)
hMG5EFT111LO.SetMarkerStyle(34)
hMG5EFT111LO.SetMarkerColor(ROOT.kBlack)
hMG5EFT111LO.SetLineColor(ROOT.kBlack)
hMG5EFT111LO.SetLineStyle(1)

# hMG5EFTcpucpBBNLO.GetYaxis().SetTitle("Nevents")
hMG5EFTcpucpBBNLO.SetStats(0)
hMG5EFTcpucpBBNLO.SetMarkerStyle(26)
hMG5EFTcpucpBBNLO.SetMarkerColor(ROOT.kBlue)
hMG5EFTcpucpBBNLO.SetLineColor(ROOT.kBlue)
hMG5EFTcpucpBBNLO.SetLineStyle(2)
#hMG5EFTcpucpBBNLO.GetYaxis().SetRangeUser(0, 1.5)

hMG5EFTcpucpBBLO.SetStats(0)
hMG5EFTcpucpBBLO.SetMarkerStyle(22)
hMG5EFTcpucpBBLO.SetMarkerColor(ROOT.kBlue)
hMG5EFTcpucpBBLO.SetLineColor(ROOT.kBlue)

c = ROOT.TCanvas()
upperPad = ROOT.TPad("upperPad", "upperPad", 0., 0.3, 1., 1.)
middlePad = ROOT.TPad("middlePad", "middlePad", 0., 0.2, 1., 0.3)
lowerPad = ROOT.TPad("lowerPad","lowerPad", 0., 0., 1., 0.2)
upperPad.Draw()
middlePad.Draw()
lowerPad.Draw()
upperPad.SetTicks(1, 1)
#upperPad.SetLogy()
upperPad.SetBottomMargin(0.)
#upperPad.SetRightMargin(0.2)
#hNLO.SetMinimum(3e-9)
#hNLO.SetMaximum(10)
upperPad.cd()

hNLO.Draw("h")
hMG5EFTcpucpBBNLO.Draw("peh same")
hMG5EFT111NLO.Draw("peh same")
hLO.Draw("peh same")
hMG5EFTcpucpBBLO.Draw("peh same")
hMG5EFT111LO.Draw("peh same")

middlePad.cd()
middlePad.SetTicks(1, 1)
middlePad.SetGridy()
middlePad.SetTopMargin(0.)
middlePad.SetBottomMargin(0.)

hRatiocpucpBBLO = ROOT.TGraphAsymmErrors()
hRatiocpucpBBLO.Divide(hMG5EFTcpucpBBLO, hLO, 'pois')
hRatiocpucpBBLO.SetMarkerStyle(22)
hRatiocpucpBBLO.SetMarkerColor(ROOT.kBlue)
hRatiocpucpBBLO.SetLineColor(ROOT.kBlue)

hRatiocpWcpWBcpq3iLO = ROOT.TGraphAsymmErrors()
hRatiocpWcpWBcpq3iLO.Divide(hMG5EFT111LO, hLO, 'pois')
hRatiocpWcpWBcpq3iLO.SetMarkerStyle(34)
hRatiocpWcpWBcpq3iLO.SetMarkerColor(ROOT.kBlack)
hRatiocpWcpWBcpq3iLO.SetLineColor(ROOT.kBlack)

hRatioMultiLO = ROOT.TMultiGraph("hRatioMultiLO", "")
hRatioMultiLO.Add(hRatiocpucpBBLO, "AP")
hRatioMultiLO.Add(hRatiocpWcpWBcpq3iLO, "AP")

hRatioMultiLO.GetXaxis().SetLimits(0, 600)
hRatioMultiLO.GetYaxis().SetNdivisions(505)
hRatioMultiLO.GetYaxis().SetRangeUser(0.7, 2)
hRatioMultiLO.GetYaxis().SetTitle("#frac{EFT}{LO}")
hRatioMultiLO.GetYaxis().SetTitleSize(0.34)
hRatioMultiLO.GetYaxis().SetLabelSize(0.38)
hRatioMultiLO.GetYaxis().SetTitleOffset(0.12)
hRatioMultiLO.Draw("AP")

lowerPad.cd()
lowerPad.SetTicks(1, 1)
lowerPad.SetGridy()
lowerPad.SetTopMargin(0.)
lowerPad.SetBottomMargin(0.5)

hRatiocpucpBB = ROOT.TGraphAsymmErrors()
hRatiocpucpBB.Divide(hMG5EFTcpucpBBNLO, hNLO, 'pois')
hRatiocpucpBB.SetMarkerStyle(26)
hRatiocpucpBB.SetMarkerColor(ROOT.kBlue)
hRatiocpucpBB.SetLineColor(ROOT.kBlue)
hRatiocpucpBB.SetLineStyle(2)

hRatiocpWcpWBcpq3i = ROOT.TGraphAsymmErrors()
hRatiocpWcpWBcpq3i.Divide(hMG5EFT111NLO, hNLO, 'pois')
hRatiocpWcpWBcpq3i.SetMarkerStyle(28)
hRatiocpWcpWBcpq3i.SetMarkerColor(ROOT.kBlack)
hRatiocpWcpWBcpq3i.SetLineColor(ROOT.kBlack)
hRatiocpWcpWBcpq3i.SetLineStyle(2)

hRatioMultiNLO = ROOT.TMultiGraph("hRatioMultiNLO", "")
hRatioMultiNLO.Add(hRatiocpucpBB, "AP")
hRatioMultiNLO.Add(hRatiocpWcpWBcpq3i, "AP")

hRatioMultiNLO.GetXaxis().SetTitleSize(0.2)
hRatioMultiNLO.GetXaxis().SetLabelSize(0.2)
hRatioMultiNLO.GetXaxis().SetTitleOffset(1)
hRatioMultiNLO.GetXaxis().SetLimits(0, 600)
hRatioMultiNLO.GetXaxis().SetTitle("p_{T}(H) [GeV]")
hRatioMultiNLO.GetYaxis().SetNdivisions(505)
hRatioMultiNLO.GetYaxis().SetRangeUser(0.7, 2)
hRatioMultiNLO.GetYaxis().SetTitle("#frac{EFT}{NLO}")
hRatioMultiNLO.GetYaxis().SetTitleSize(0.17)
hRatioMultiNLO.GetYaxis().SetLabelSize(0.19)
hRatioMultiNLO.GetYaxis().SetTitleOffset(0.22)
hRatioMultiNLO.Draw("AP")

upperPad.cd()
leg = ROOT.TLegend(0.263, 0.45, 0.87, 0.85)
leg.SetBorderSize(0)
leg.AddEntry(hLO, "MadGraph5 (LO, SM)", "PEL")
leg.AddEntry(hNLO, "POWHEG V2 (NLO, SM)", "PEL")
leg.AddEntry(hMG5EFTcpucpBBLO, "#splitline{MG5_SMEFT@LO + Pythia8}{cpu=cpBB=0.1}", "PEL")
leg.AddEntry(hMG5EFTcpucpBBNLO, "#splitline{MG5_SMEFT@NLO + Pythia8}{cpu=cpBB=0.1}", "PEL")
leg.AddEntry(hMG5EFT111LO, "#splitline{MG5_SMEFT@LO + Pythia8}{cpW=cpWB=cpq3i=0.1}", "PEL")
leg.AddEntry(hMG5EFT111NLO, "#splitline{MG5_SMEFT@NLO + Pythia8}{cpW=cpWB=cpq3i=0.1}", "PEL")
'''
leg.AddEntry(hRatiocpucpBBLO, "cpu=cpBB=0.1(LO)/SM(LO)", "PE")
leg.AddEntry(hRatiocpucpBB, "cpu=cpBB=0.1(NLO)/SM(NLO)", "PE")
leg.AddEntry(hRatiocpWcpWBcpq3iLO, "cpW=cpWB=cpq3i=0.1(LO)/SM(LO)", "PE")
leg.AddEntry(hRatiocpWcpWBcpq3i, "cpW=cpWB=cpq3i=0.1(NLO)/SM(NLO)", "PE")
'''
leg.SetNColumns(2)
leg.SetTextSize(0.04)
leg.Draw("same")

c.SaveAs("./ratio_LO_NLO.pdf")