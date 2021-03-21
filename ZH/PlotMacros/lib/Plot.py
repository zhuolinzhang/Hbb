import ROOT
import re
import numpy as np

def read_data(data_list, data_mu_list, data_selection_list, data_kine_list, data_kine_dict):
    for s in data_selection_list:
        exec('h_RecDiMuon_{0}_M = ROOT.TH1F("h_RecDiMuon_{0}_M", "h_RecDiMuon_{0}_M", 60, 75, 105)'.format(s))
    for i in data_mu_list:
        for j in data_selection_list:
            for k in data_kine_list:
                for key, value in data_kine_dict.items():
                    if key == k:
                        exec('h_{0}_{1}_{2} = ROOT.TH1F("h_{0}_{1}_{2}", "h_{0}_{1}_{2}", {3})'.format(i, j, k, value))
    for d in data_list:
        for s in data_selection_list:
            exec('h_Get_RecDiMuon_{0}_M = d.Get("demo/h_RecDiMuon_{0}_M")'.format(s))
            exec('h_RecDiMuon_{0}_M += h_Get_RecDiMuon_{0}_M'.format(s))
        for i in data_mu_list:
            for j in data_selection_list:
                for k in data_kine_list:
                    exec('h_Get_{0}_{1}_{2} = d.Get("demo/h_{0}_{1}_{2}")'.format(i, j, k))
                    exec('h_{0}_{1}_{2} += h_Get_{0}_{1}_{2}'.format(i, j, k))
    data_TH1F_list = []
    for s in data_selection_list:
        exec('data_TH1F_list.append(h_RecDiMuon_{0}_M)'.format(s))
    for i in data_mu_list:
        for j in data_selection_list:
            for k in data_kine_list:
                exec('data_TH1F_list.append(h_{0}_{1}_{2})'.format(i, j, k))
    return data_TH1F_list

def scale_hist(hist, scale_factor):
    # Normalize histograms to a specific integrated luminosity
    hist.Scale(scale_factor)
    hist_entries = int(hist.GetEntries() * scale_factor)
    hist.SetEntries(hist_entries)

def plot_hist(hist):
    # Plot histrograms for each category
    c1 = ROOT.TCanvas()
    hist.SetTitle(hist.GetName())
    hist.Draw("HIST")
    c1.SaveAs("Figures/{}.pdf".format(hist.GetName()))

def stack_fill(hist, color, stack):
    # Fill histograms to THStack
    hist.SetFillColor(color)
    hist.SetLineColor(ROOT.kBlack)
    stack.Add(hist)

def make_ratio(hist_pass, hist_total, option = 'pois'):
    # make Data/MC graph and set the style of the graph
    ratio = ROOT.TGraphAsymmErrors()
    ratio.Divide(hist_pass, hist_total, option) # the defalut option in ROOT is 'cp'(Gauss case)
    ratio.GetYaxis().SetTitle("Data/MC")
    ratio.Draw("AP")
    ratio.GetYaxis().SetNdivisions(505)
    ratio.SetMaximum(2.49)
    ratio.SetMinimum(0.)
    ratio.SetMarkerStyle(20)
    ratio.GetYaxis().SetTitleSize(0.08)
    ratio.GetXaxis().SetTitleSize(0.1)
    ratio.GetXaxis().SetLabelSize(0.08)
    ratio.GetXaxis().SetTitleOffset(1)
    ratio.GetYaxis().SetLabelSize(0.08)
    ratio.GetYaxis().SetTitleOffset(0.4)
    return ratio
    
def plot_ratio(hist_sig, hist_bkg1, hist_bkg2, hist_bkg3, hist_bkg4, hist_bkg5, stack_name, data_TH1F_list):
    # Plot the stack histogram and Data/MC
    # Sum MC samples and create MC Stat. Err. graphs
    sum_hist = hist_sig + hist_bkg1 + hist_bkg2 + hist_bkg3 + hist_bkg4 + hist_bkg5
    stack_err = ROOT.TGraphErrors(sum_hist) # MC. Stat. Err.
    rel_err_hist = stack_err.Clone("rel_err_hist") # MC. relative Stat. Err.

    # Fill TGraphErrors(MC relative Stat. Err.)
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
    
    # Create TCanvas and two TPads to place THStack and Data/MC
    c2 = ROOT.TCanvas("c2", "", 800, 600)
    upperPad = ROOT.TPad("upperPad", "upperPad", 0., 0.3, 1. , 1.)
    lowerPad = ROOT.TPad("lowerPad", "lowerPad", 0., 0., 1. , 0.3)
    upperPad.Draw()
    lowerPad.Draw()
    upperPad.SetTicks(1, 1)
    upperPad.SetLogy()
    upperPad.SetBottomMargin(0.)
    upperPad.cd() # active uppper pad
    # Fill THStack and set the style of THStack
    hs = ROOT.THStack("hs","{}".format(stack_name))
    stack_fill(hist_sig, ROOT.kYellow + 1, hs)
    stack_fill(hist_bkg1, ROOT.kBlue, hs)
    stack_fill(hist_bkg2, ROOT.kGray + 2, hs)
    stack_fill(hist_bkg3, ROOT.kGreen + 1, hs)
    stack_fill(hist_bkg4, ROOT.kViolet - 2, hs)
    stack_fill(hist_bkg5, ROOT.kRed + 1, hs)
    hs.Draw("HIST")
    hs.SetMinimum(1e-1)
    hs.SetMaximum(3e8)
    hs.GetYaxis().SetTitleOffset(1)
    hs.GetYaxis().SetTitle("Events / {:.1f}".format(sum_hist.GetXaxis().GetBinWidth(1)))

    # Plot the MC Stat. Err. and set the style of MC Stat. Err.
    stack_err.SetFillStyle(3013)
    stack_err.SetFillColor(ROOT.kBlack)
    stack_err.Draw("2")

    # Plot data points
    for i in data_TH1F_list:
        if re.search(stack_name, i.GetName()):
            data_hist = i
    data_hist.SetMarkerStyle(20)
    data_hist.SetStats(0) # avoid the statistics box is drawn after plot_hist the data histograms
    data_hist.Draw("SAME E0")
    '''
    # Check the match of THStack and data are right
    print("------------------")
    print("The data hist name: ", data_hist.GetName())
    print("The stack name: ", stack_name)
    print("------------------")
    '''

    # Set the legend of THStack
    leg = ROOT.TLegend(0.63, 0.70, 0.86, 0.87)
    leg.AddEntry(data_hist, "Data", "P")
    leg.AddEntry(hist_bkg5, "Z+jets", "F")
    leg.AddEntry(hist_bkg4, "QCD", "F")
    leg.AddEntry(hist_bkg3, "ZZ", "F")
    leg.AddEntry(hist_bkg1, "Single top", "F")
    leg.AddEntry(hist_bkg2, "t#bar{t}", "F")
    leg.AddEntry(hist_sig, "ZH(b#bar{b})", "F")
    leg.AddEntry(stack_err, "MC Stat. Error", "F")
    leg.SetNColumns(2)
    leg.SetBorderSize(0)
    leg.Draw("SAME")

    # Set the CMS label, collision energy and integrated luminosity
    fig_lable = ROOT.TLatex()
    fig_lable.SetTextSize(.03)
    fig_lable.DrawLatexNDC(.7, .91, "#sqrt{s} = 13 TeV, L = 59.74 fb^{-1}")
    fig_lable.DrawLatexNDC(.1, .91, "#scale[1.2]{CMS} #font[52]{Preliminary}")

    # Set the style of lower pad (MC relative Stat. Err. and Data/MC)
    lowerPad.cd() # active lower pad
    lowerPad.SetTicks(1, 1)
    lowerPad.SetGridy()
    lowerPad.SetTopMargin(0.)
    lowerPad.SetBottomMargin(0.3)
    ratio = make_ratio(data_hist, sum_hist)
    ratio.GetXaxis().SetLimits(data_hist.GetXaxis().GetXmin(), data_hist.GetXaxis().GetXmax())
    rel_err_hist.SetFillStyle(3013)
    rel_err_hist.SetFillColor(ROOT.kBlack)
    rel_err_hist.Draw("2")
    if re.search('_M', stack_name):
        ratio.GetXaxis().SetTitle("m_{#mu^{+}#mu^{-}} [GeV]")
    if re.search('pt', stack_name):
        ratio.GetXaxis().SetTitle("p_{T} [GeV]")
    if re.search('eta', stack_name):
        ratio.GetXaxis().SetTitle("#eta")
    if re.search('phi', stack_name):
        ratio.GetXaxis().SetTitle("#phi")
    
    c2.SaveAs("Stacks/stack_{}.pdf".format(stack_name))