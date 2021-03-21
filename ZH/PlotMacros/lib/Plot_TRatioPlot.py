import ROOT
import re
import numpy as np

def scale_hist(hist, scale_factor):
    # Normalize histograms to a specific integrated luminosity
    hist.Scale(scale_factor)
    hist_entries = int(hist.GetEntries() * scale_factor)
    hist.SetEntries(hist_entries)

def plot_hist(hist):
    # Plot histrograms for each category
    c1 = ROOT.TCanvas()
    hist.SetTitle(hist.GetName())
    if re.search("h_", hist.GetName()):
        c1.SetLogy()
        hist.SetMarkerStyle(20)
        hist.SetMinimum(1e-1)
        hist.SetMaximum(1e8)
    hist.Draw("HIST")
    c1.SaveAs("Figures/{}.pdf".format(hist.GetName()))

def stack_fill(hist, color, stack):
    # Fill histograms to THStack
    hist.SetFillColor(color)
    hist.SetLineColor(ROOT.kBlack)
    stack.Add(hist)

def plot_ratio(hist_sig, hist_bkg1, hist_bkg2, hist_bkg3, hist_bkg4, hist_bkg5, stack_name, data_TH1F_list):
    c2 = ROOT.TCanvas()
    ROOT.gStyle.SetOptStat(0000)
    # Plot the stack histogram
    sum_hist = hist_sig + hist_bkg1 + hist_bkg2 + hist_bkg3 + hist_bkg4 + hist_bkg5
    stack_err = ROOT.TGraphErrors(sum_hist)
    rel_err_hist = stack_err.Clone("rel_err_hist")
    # Set the parameters for TGraphErrors
    for i in range(0, rel_err_hist.GetN()):
        n = i + 1
        point_y = rel_err_hist.GetPointY(n)
        point_err_y = rel_err_hist.GetErrorY(n)
        if point_y == 0:
            rel_err_y = 0
        else:
            rel_err_y = point_err_y / point_y
        rel_err_hist.SetPointY(n, 1.)
        rel_err_hist.SetPointError(n, rel_err_hist.GetErrorX(n), rel_err_y)

    # Plot data points
    for i in data_TH1F_list:
        if re.search(stack_name, i.GetName()):
            data_hist = i
    data_hist.SetMarkerStyle(20)
    #data_hist.Draw("SAME E0")
    '''
    # Check the match is right
    print("------------------")
    print("The data hist name: ", data_hist.GetName())
    print("The stack name: ", stack_name)
    print("------------------")
    '''
    data_hist.SetMinimum(0)
    #data_hist.SetMaximum(1e8)
    data_hist.SetTitle(stack_name)
    ratio = ROOT.TRatioPlot(data_hist, sum_hist)
    ratio.SetH1DrawOpt("P")
    ratio.SetSeparationMargin(0.0)
    lines = np.array(1.)
    ratio.SetGridlines(lines)
    ratio.Draw()
    fig_lable = ROOT.TLatex()
    fig_lable.SetTextSize(.03)
    fig_lable.DrawLatex(.15, .9, "#sqrt{s} = 13 TeV, L = 59.74 fb^{-1}")

    if re.search('_M', stack_name):
        data_hist.GetXaxis().SetLimits(75, 105)
        sum_hist.GetXaxis().SetLimits(75, 105)
        ratio.GetLowerRefGraph().GetXaxis().SetLimits(75, 105)
        data_hist.GetXaxis().SetTitle("m_{#mu^{+}#mu^{-}}")
        ratio.GetUpperRefYaxis().SetTitle("Events / 0.5 GeV")
    if re.search('pt', stack_name):
        data_hist.GetXaxis().SetLimits(0, 500)
        sum_hist.GetXaxis().SetLimits(0, 500)
        ratio.GetLowerRefGraph().GetXaxis().SetLimits(0, 500)
        data_hist.GetXaxis().SetTitle("p_{T}")
        ratio.GetUpperRefYaxis().SetTitle("Events / 1 GeV")
    if re.search('eta', stack_name):
        data_hist.GetXaxis().SetLimits(-6, 6)
        sum_hist.GetXaxis().SetLimits(-6, 6)
        ratio.GetLowerRefGraph().GetXaxis().SetLimits(-6, 6)
        data_hist.GetXaxis().SetTitle("#eta")
        ratio.GetUpperRefYaxis().SetTitle("Events / 0.1")
    if re.search('phi', stack_name):
        data_hist.GetXaxis().SetLimits(-4, 4)
        sum_hist.GetXaxis().SetLimits(-4, 4)
        ratio.GetLowerRefGraph().GetXaxis().SetLimits(-4, 4)
        data_hist.GetXaxis().SetTitle("#phi")
        ratio.GetUpperRefYaxis().SetTitle("Events / 0.1")
    
    #ratio.GetUpperRefYaxis().SetTitleOffset(1)
    ratio.GetLowerRefYaxis().SetTitle("Data/MC")
    #ratio.GetLowerRefYaxis().SetTitleSize(0.08)
    #ratio.GetLowerRefYaxis().SetTitleOffset(0.4)
    #ratio.GetLowerRefYaxis().SetLabelSize(0.05)
    #ratio.GetLowerRefYaxis().SetNdivisions(210)
    ratio.GetLowerRefGraph().SetMinimum(0)
    ratio.GetLowerRefGraph().SetMaximum(2.5)
    ratio.GetLowerRefGraph().SetMarkerStyle(20)
    
    hs = ROOT.THStack("hs",stack_name)

    stack_fill(hist_sig, ROOT.kYellow + 1, hs)
    stack_fill(hist_bkg1, ROOT.kBlue, hs)
    stack_fill(hist_bkg2, ROOT.kGray + 2, hs)
    stack_fill(hist_bkg3, ROOT.kGreen + 1, hs)
    stack_fill(hist_bkg4, ROOT.kViolet - 2, hs)
    stack_fill(hist_bkg5, ROOT.kRed + 1, hs)

    stack_err.SetFillStyle(3013)
    stack_err.SetFillColor(ROOT.kBlack)

    ratio.GetUpperPad().cd()
    hs.Draw("HIST SAME")
    stack_err.Draw("2")
    data_hist.Draw("SAME P E0")
    
    # Set the legend of THStack
    leg = ROOT.TLegend(0.75, 0.77, 0.9, 0.9)
    leg.AddEntry(data_hist, "Data", "P")
    leg.AddEntry(hist_bkg5, "Z+jets", "F")
    leg.AddEntry(hist_bkg4, "QCD", "F")
    leg.AddEntry(hist_bkg3, "VV", "F")
    leg.AddEntry(hist_bkg1, "Single top", "F")
    leg.AddEntry(hist_bkg2, "t#bar{t}", "F")
    leg.AddEntry(hist_sig, "ZH(b#bar{b})", "F")
    leg.AddEntry(stack_err, "MC Stat. Error", "F")
    leg.SetNColumns(2)
    leg.Draw("SAME")
    
    ratio.GetLowerPad().cd()

    #rel_err_hist.SetMarkerStyle(7)
    rel_err_hist.SetFillStyle(3013)
    rel_err_hist.SetFillColor(ROOT.kBlack)
    rel_err_hist.Draw("2")

    #ratio.GetUpperPad().SetLogy()
    ratio.GetUpperPad().Update()
    c2.SaveAs("Stacks/stack_{}.pdf".format(stack_name))
    #c2.Write()