import ROOT
import os
from array import array

def open_root_files(dirPath):
    # Load root files in a folder
    dirList = os.listdir(dirPath)
    rootFileList = []
    for fileName in dirList:
        fileFullPath = dirPath + '/' + fileName
        f = ROOT.TFile(fileFullPath)
        if f.IsZombie(): continue # to make sure f is a valid .root file
        rootFileList.append(f)
    return rootFileList

def get_primary_name(rootFile):
    # Because in my analysis, the .root file is named by the primary dataset name. 
    # This function actually get the primary dataset name.
    fileFullPath = rootFile.GetName()
    fileName = fileFullPath.split('/')[-1]
    datasetName = fileName.rstrip('.root')
    return datasetName

def plot_hist(hist):
    # Plot histrograms for each category
    if os.path.exists('./figure'): pass
    else: os.mkdir('./figure')
    c1 = ROOT.TCanvas()
    hist.SetTitle(hist.GetName())
    hist.Draw("HIST")
    c1.SaveAs("figure/{}.pdf".format(hist.GetName()))

def stack_fill(hist, stack):
    # Fill histograms to THStack
    color_dict = {'st': ROOT.kAzure + 8, 'tt': ROOT.kAzure + 4, 'zz': ROOT.kSpring + 2, 'qcd': ROOT.kViolet - 4, 'zjets': ROOT.kOrange - 2}
    findHist = False
    for key, value in color_dict.items():
        if key in hist.GetName():
            hist.SetFillColor(value)
            findHist = True
    if findHist == True:
        hist.SetLineColor(ROOT.kBlack)
        stack.Add(hist)

def make_ratio(hist_pass, hist_total, option = 'pois'):
    # make Data/MC or Sideband/SR graph and set the style of the graph
    ratio = ROOT.TGraphAsymmErrors()
    ratio.Divide(hist_pass, hist_total, option) # the defalut option in ROOT is 'cp'(Gauss case)
    ratio.Draw("AP")
    ratio.GetYaxis().SetNdivisions(505)
    ratio.SetMaximum(2.49)
    ratio.SetMinimum(0.01)
    ratio.GetYaxis().SetTitleSize(0.08)
    ratio.GetXaxis().SetTitleSize(0.1)
    ratio.GetXaxis().SetLabelSize(0.08)
    ratio.GetXaxis().SetTitleOffset(1)
    ratio.GetYaxis().SetLabelSize(0.08)
    ratio.GetYaxis().SetTitleOffset(0.4)
    return ratio

def make_legend(legend, hist, errHist, sigHist):
    # Make the legend in THStack.
    # The sigHist is provided when we need to plot the signal sample on the THStack after scaling.
    histLegDict = {'st': "Single top", 'tt': "t#bar{t}", 'zz': "ZZ", 'qcd': "QCD", 'zjets': "Z+jets", 'zh': 'ZH(b#bar{b})'}
    for i in hist:
        if 'data' in i.GetName():
            legend.AddEntry(i, "Data", "PE")
            continue
        if 'sumSideband' in i.GetName():
            legend.AddEntry(i, "Total Sideband", "PE")
            continue
        for key, value in histLegDict.items():
            if key in i.GetName():
                if 'zh' in i.GetName(): continue
                legend.AddEntry(i, value, "F")
    legend.AddEntry(errHist, "MC Stat. Error", "F")
    legend.AddEntry(sigHist, "ZH(b#bar{b}) x 500", "L")
    legend.SetNColumns(2)
    legend.SetBorderSize(0)
    
def plot_ratio(stackType, stackName, *hist):
    # Plot the stack histogram and Data/MC
    # Sum MC samples and create MC Stat. Err. graphs
    for i in hist:
        if 'zh' in i.GetName():
            sigHist = i.Clone() # If we don't use TH1::Clone, the legend of signal stack will be wrong.
    sumHist = sigHist
    dataNevents = 0
    for i in hist:
        if 'data' in i.GetName(): 
            dataNevents = i.Integral()
            continue
        if 'sumSideband' in i.GetName(): 
            dataNevents = i.Integral()
            continue
        if 'zh' in i.GetName(): continue
        sumHist += i
    
    if stackType == 'mcData':
        print("Stack: {}\tNevents in Signal: {:.3f}\tNevents in Data: {:.0f}".format(stackName, sigHist.Integral(), dataNevents))
    elif stackType == 'srSideband':
        print("Stack: {}\tNevents in Signal: {:.3f}\tNevents in Sideband: {:.3f}".format(stackName, sigHist.Integral(), dataNevents))
    '''
    nTT = 0
    nZjets = 0
    for i in hist:
        if 'tt' in i.GetName(): nTT = i.Integral()
        if 'zjets' in i.GetName(): nZjets = i.Integral()
    print("Stack: {}\tNevents in ttbar: {:.3f}\tNevents in z+jets: {:.3f}".format(stackName, nTT, nZjets))
    '''
    stackErr = ROOT.TGraphErrors(sumHist) # MC. Stat. Err.
    #rel_err_hist = stackErr.Clone("rel_err_hist") # MC. relative Stat. Err.
    relErr = ROOT.TGraphErrors(sumHist.GetNbinsX())
    relErr.SetTitle("")
    # Fill TGraphErrors(MC relative Stat. Err.)
    '''
    for i in range(0, rel_err_hist.GetN()):
        n = i + 1
        pointY = rel_err_hist.GetPointY(n)
        pointErrY = rel_err_hist.GetErrorY(n)
        if pointY == 0:
            relErrY = 0
        else:
            relErrY = pointErrY / pointY
        rel_err_hist.SetPointY(n, 1.)
        rel_err_hist.SetPointError(n, rel_err_hist.GetErrorX(n), relErrY)
    '''
    for i in range(0, sumHist.GetNbinsX()):
        n = i + 1
        pointY = sumHist.GetBinContent(n)
        pointErrY = sumHist.GetBinError(n)
        if pointY == 0:
            relErrY = 0
        else:
            relErrY = pointErrY / pointY
        relErr.SetPoint(n, sumHist.GetXaxis().GetBinCenter(n), 1.)
        relErr.SetPointError(n, sumHist.GetBinWidth(n) / 2, relErrY)

    # Create TCanvas and two TPads to place THStack and Data/MC
    c = ROOT.TCanvas("c", "", 800, 600)
    upperPad = ROOT.TPad("upperPad", "upperPad", 0., 0.3, 1. , 1.)
    lowerPad = ROOT.TPad("lowerPad", "lowerPad", 0., 0., 1. , 0.3)
    upperPad.Draw()
    lowerPad.Draw()
    upperPad.SetTicks(1, 1)
    upperPad.SetLogy()
    upperPad.SetBottomMargin(0.)
    upperPad.cd() # active uppper pad
    # Fill THStack and set the style of THStack
    hs = ROOT.THStack("hs","")
    for i in hist:
        if 'zh' in i.GetName(): continue
        stack_fill(i, hs)
    hs.Draw("HIST")
    hs.SetMinimum(1e-3)
    hs.SetMaximum(3e3)
    hs.GetYaxis().SetTitleOffset(1)
    hs.GetYaxis().SetTitle("Events / {:.1f}".format(sumHist.GetXaxis().GetBinWidth(1)))
    if '_Pt' in stackName:
        hs.GetYaxis().SetTitle("Events")

    # Plot the MC Stat. Err. and set the style of MC Stat. Err.
    stackErr.SetFillStyle(3013)
    stackErr.SetFillColor(ROOT.kBlack)
    stackErr.SetLineColor(ROOT.kBlack)
    stackErr.Draw("2")
    
    sigHist.Scale(500)
    sigHist.SetLineColor(ROOT.kRed)
    sigHist.SetMarkerColor(ROOT.kRed)
    sigHist.SetLineWidth(2)
    sigHist.Draw("SAME HIST ][")
    
    # Plot data points
    dataHist = ROOT.TH1F()
    for i in hist:
        if 'data' in i.GetName():
            dataHist = i
        if 'sumSideband' in i.GetName():
            dataHist = i
    if stackType == 'mcData':
        dataHist.SetMarkerStyle(20)
    elif stackType == 'srSideband':
        dataHist.SetMarkerStyle(24)
    dataHist.SetStats(0) # avoid the statistics box is drawn after plot_hist the data histograms
    dataHist.SetLineColor(ROOT.kBlack)
    dataHist.Draw("SAME E0")

    # Set the legend of THStack
    leg = ROOT.TLegend(0.63, 0.70, 0.86, 0.87)
    make_legend(leg, hist, stackErr, sigHist)
    leg.Draw("SAME")

    # Set the CMS label, collision energy and integrated luminosity
    fig_lable = ROOT.TLatex()
    fig_lable.SetTextSize(.03)
    data_lumi = 0.271
    fig_lable.DrawLatexNDC(.75, .91, "#font[42]{13 TeV (%s fb^{-1})}" % data_lumi)
    if stackType == 'mcData':
        fig_lable.DrawLatexNDC(.1, .91, "#scale[1.2]{CMS} #font[52]{Preliminary}")
    else:
        fig_lable.DrawLatexNDC(.1, .91, "#scale[1.2]{CMS} #font[52]{Simulation Preliminary}")

    # Set the style of lower pad (MC relative Stat. Err. and Data/MC)
    lowerPad.cd() # active lower pad
    lowerPad.SetTicks(1, 1)
    lowerPad.SetGridy()
    lowerPad.SetTopMargin(0.)
    lowerPad.SetBottomMargin(0.3)
    if stackType == 'mcData' or stackType == 'srSideband':
        ratio = make_ratio(dataHist, sumHist)
        ratio.GetXaxis().SetLimits(dataHist.GetXaxis().GetXmin(), dataHist.GetXaxis().GetXmax())
        ratio.GetYaxis().SetTitle("Sideband/SR")
        ratio.SetMarkerStyle(24)
        if stackType == 'mcData':
            ratio.GetYaxis().SetTitle("Data/MC")
            ratio.SetMarkerStyle(20)
            relErr.SetFillStyle(3013)
            relErr.SetFillColor(ROOT.kBlack)
            relErr.Draw("2")
    else:
        ratio = relErr
        ratio.GetXaxis().SetLimits(sumHist.GetXaxis().GetXmin(), sumHist.GetXaxis().GetXmax())
        ratio.SetFillStyle(3013)
        ratio.SetFillColor(ROOT.kBlack)
        ratio.GetYaxis().SetTitle("Relative Errors")
        ratio.Draw("A2")
        ratio.GetYaxis().SetNdivisions(505)
        ratio.SetMaximum(2.49)
        ratio.SetMinimum(0.01)
        ratio.SetMarkerStyle(20)
        ratio.GetYaxis().SetTitleSize(0.08)
        ratio.GetXaxis().SetTitleSize(0.1)
        ratio.GetXaxis().SetLabelSize(0.08)
        ratio.GetXaxis().SetTitleOffset(1)
        ratio.GetYaxis().SetLabelSize(0.08)
        ratio.GetYaxis().SetTitleOffset(0.4)
    
    if "DiJet" in stackName:
        if '_M' in stackName:
            ratio.GetXaxis().SetTitle("m_{DiJet} [GeV]")
        if 'Pt' in stackName:
            ratio.GetXaxis().SetTitle("p_{T}^{DiJet} [GeV]")
        if 'Eta' in stackName:
            ratio.GetXaxis().SetTitle("#eta_{DiJet}")
        if 'Phi' in stackName:
            ratio.GetXaxis().SetTitle("#phi_{DiJet}")
    elif "DiMuon" in stackName:
        if '_M' in stackName:
            ratio.GetXaxis().SetTitle("m_{DiMuon} [GeV]")
        if 'Pt' in stackName:
            ratio.GetXaxis().SetTitle("p_{T}^{DiMuon} [GeV]")
        if 'Eta' in stackName:
            ratio.GetXaxis().SetTitle("#eta_{DiMuon}")
        if 'Phi' in stackName:
            ratio.GetXaxis().SetTitle("#phi_{DiMuon}")

    c.SaveAs("stack/{}.pdf".format(stackName))

def write_to_root(objName, kiniName, *hist):
    sumBkgHist = ROOT.TH1F()
    if kiniName == 'Pt':
        edgeArray = array('d', [0, 10, 20, 30, 40, 50, 60, 80, 100, 120,
                                140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 500])
        sumBkgHist = ROOT.TH1F("sumBkgHist", "sumBkgHist", 21, edgeArray)
    for i in hist:
        if 'zh' in i.GetName():
            sigHist = i.Clone()
    for i in hist:
        if 'zh' in i.GetName():
            continue
        if 'data' in i.GetName():
            continue
        sumBkgHist += i
    sigHist.SetName("sigHist")
    sumBkgHist.SetName("sumBkgHist")
    #sumBkgHist.GetXaxis().SetLimits(sigHist.GetXaxis().GetXmin(), sigHist.GetXaxis().GetXmax())
    f = ROOT.TFile("./stack/{}_{}.root".format(objName, kiniName), "RECREATE")
    sigHist.Write()
    sumBkgHist.Write()
    f.Close()