import ROOT
import re
import numpy as np

def read_data(data_list, data_mu_list, data_selection_list, data_kine_list, data_kine_dict):
    for s in data_selection_list:
        exec('h_RecDiMuon_{0}_M = ROOT.TH1F("h_RecDiMuon_{0}_M", "h_RecDiMuon_{0}_M", 60, 75, 105)'.format(s))
        exec('h_RecDiJet_{0}_M = ROOT.TH1F("h_RecDiJet_{0}_M", "h_RecDiJet_{0}_M", 75, 50, 200)'.format(s))
    for i in data_mu_list:
        for j in data_selection_list:
            for k in data_kine_list:
                for key, value in data_kine_dict.items():
                    if key == k:
                        exec('h_{0}_{1}_{2} = ROOT.TH1F("h_{0}_{1}_{2}", "h_{0}_{1}_{2}", {3})'.format(i, j, k, value))
    for d in data_list:
        for s in data_selection_list:
            exec('h_Get_RecDiMuon_{0}_M = d.Get("h_RecDiMuon_{0}_M")'.format(s))
            exec('h_RecDiMuon_{0}_M += h_Get_RecDiMuon_{0}_M'.format(s))
            exec('h_Get_RecDiJet_{0}_M = d.Get("h_RecDiJet_{0}_M")'.format(s))
            exec('h_RecDiJet_{0}_M += h_Get_RecDiJet_{0}_M'.format(s))
        for i in data_mu_list:
            for j in data_selection_list:
                for k in data_kine_list:
                    exec('h_Get_{0}_{1}_{2} = d.Get("h_{0}_{1}_{2}")'.format(i, j, k))
                    exec('h_{0}_{1}_{2} += h_Get_{0}_{1}_{2}'.format(i, j, k))
    data_TH1F_list = []
    # blind the signal region
    for s in data_selection_list:
        for i in range(20, 50):
            exec('h_RecDiJet_{}_M.SetBinContent({}, 0)'.format(s, i))
    
    for s in data_selection_list:
        exec('data_TH1F_list.append(h_RecDiMuon_{0}_M)'.format(s))
        exec('data_TH1F_list.append(h_RecDiJet_{0}_M)'.format(s))
    for i in data_mu_list:
        for j in data_selection_list:
            for k in data_kine_list:
                exec('data_TH1F_list.append(h_{0}_{1}_{2})'.format(i, j, k))
    return data_TH1F_list

def scale_hist(hist, scale_factor):
    # Normalize histograms to a specific integrated luminosity
    scale_factor = scale_factor * 0.004536324 # correct to ref. trigger
    hist.Scale(scale_factor)
    hist_entries = hist.GetEntries() * scale_factor
    hist.SetEntries(hist_entries)

def plot_hist(hist):
    # Plot histrograms for each category
    c1 = ROOT.TCanvas()
    hist.SetTitle(hist.GetName())
    hist.Draw("HIST")
    c1.SaveAs("Figures/{}.pdf".format(hist.GetName()))

def stack_fill(hist, stack):
    # Fill histograms to THStack
    color_dict = {'st': ROOT.kBlue, 'tt': ROOT.kGray + 2, 'dib': ROOT.kGreen + 1, 'qcd': ROOT.kViolet - 2, 'zjets': ROOT.kYellow + 1}
    if re.search('sig', '{}'.format(hist)):
        hist.SetFillColor(ROOT.kRed + 1)
        hist.SetLineColor(ROOT.kBlack)
        stack.Add(hist)
    else:
        for i in hist:
            for key, value in color_dict.items():
                if re.search(key, '{}'.format(i)):
                    i.SetFillColor(value)
            i.SetLineColor(ROOT.kBlack)
            stack.Add(i)

def make_ratio(hist_pass, hist_total, option = 'pois'):
    # make Data/MC graph and set the style of the graph
    ratio = ROOT.TGraphAsymmErrors()
    ratio.Divide(hist_pass, hist_total, option) # the defalut option in ROOT is 'cp'(Gauss case)
    ratio.GetYaxis().SetTitle("Data/MC")
    ratio.Draw("AP")
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
    return ratio

def make_legend(legend, hist_sig, hist_bkg_list, err_hist, data_hist = None):
    # We must notice that the result of read_data is a list. Here we input data_hist which should be a TH1 histogram to this function.
    bkg_leg_dict = {'st': "Single top", 'tt': "t#bar{t}", 'dib': "ZZ", 'qcd': "QCD", 'zjets': "Z+jets"}
    if data_hist != None:
        legend.AddEntry(data_hist, "Data", "P")
    legend.AddEntry(hist_sig, "ZH(b#bar{b})", "F")
    legend.AddEntry(err_hist, "MC Stat. Error", "F")
    for i in hist_bkg_list:
        for key, value in bkg_leg_dict.items():
            if re.search(key, '{}'.format(i)):
                legend.AddEntry(i, value, "F")
    legend.SetNColumns(2)
    legend.SetBorderSize(0)
    
def plot_ratio(hist_sig, hist_bkg_list, stack_name, data_TH1F_list = None):
    # Plot the stack histogram and Data/MC
    # Sum MC samples and create MC Stat. Err. graphs
    sum_hist = hist_sig
    for i in hist_bkg_list:
        sum_hist += i
    stack_err = ROOT.TGraphErrors(sum_hist) # MC. Stat. Err.
    #rel_err_hist = stack_err.Clone("rel_err_hist") # MC. relative Stat. Err.
    rel_err_hist = ROOT.TGraphErrors(sum_hist.GetNbinsX())
    rel_err_hist.SetTitle("")
    # Fill TGraphErrors(MC relative Stat. Err.)
    '''
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
    '''
    for i in range(0, sum_hist.GetNbinsX()):
        n = i + 1
        point_y = sum_hist.GetBinContent(n)
        point_err_y = sum_hist.GetBinError(n)
        if point_y == 0:
            rel_err_y = 0
        else:
            rel_err_y = point_err_y / point_y
        rel_err_hist.SetPoint(n, sum_hist.GetXaxis().GetBinCenter(n), 1.)
        rel_err_hist.SetPointError(n, sum_hist.GetBinWidth(n) / 2, rel_err_y)

    
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
    hs = ROOT.THStack("hs","")
    stack_fill(hist_sig, hs)
    stack_fill(hist_bkg_list, hs)
    hs.Draw("HIST")
    hs.SetMinimum(1e-3)
    hs.SetMaximum(3e3)
    hs.GetYaxis().SetTitleOffset(1)
    hs.GetYaxis().SetTitle("Events / {:.1f}".format(sum_hist.GetXaxis().GetBinWidth(1)))

    # Plot the MC Stat. Err. and set the style of MC Stat. Err.
    stack_err.SetFillStyle(3013)
    stack_err.SetFillColor(ROOT.kBlack)
    stack_err.SetLineColor(ROOT.kBlack)
    stack_err.Draw("2")

    # Plot data points
    if data_TH1F_list != None:
        for i in data_TH1F_list:
            if re.search(stack_name, i.GetName()):
                data_hist = i
        data_hist.SetMarkerStyle(20)
        data_hist.SetStats(0) # avoid the statistics box is drawn after plot_hist the data histograms
        data_hist.SetLineColor(ROOT.kBlack)
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
    make_legend(leg, hist_sig, hist_bkg_list, stack_err)
    leg.Draw("SAME")

    # Set the CMS label, collision energy and integrated luminosity
    fig_lable = ROOT.TLatex()
    fig_lable.SetTextSize(.03)
    data_lumi = 0.271
    fig_lable.DrawLatexNDC(.75, .91, "#font[42]{13 TeV (%s fb^{-1})}" % data_lumi)
    if data_TH1F_list != None:
        fig_lable.DrawLatexNDC(.1, .91, "#scale[1.2]{CMS} #font[52]{Preliminary}")
    else:
        fig_lable.DrawLatexNDC(.1, .91, "#scale[1.2]{CMS} #font[52]{Simulation Preliminary}")

    # Set the style of lower pad (MC relative Stat. Err. and Data/MC)
    lowerPad.cd() # active lower pad
    lowerPad.SetTicks(1, 1)
    lowerPad.SetGridy()
    lowerPad.SetTopMargin(0.)
    lowerPad.SetBottomMargin(0.3)
    if data_TH1F_list != None:
        ratio = make_ratio(data_hist, sum_hist)
        ratio.GetXaxis().SetLimits(data_hist.GetXaxis().GetXmin(), data_hist.GetXaxis().GetXmax())
        rel_err_hist.SetFillStyle(3013)
        rel_err_hist.SetFillColor(ROOT.kBlack)
        rel_err_hist.Draw("2")
    else:
        ratio = rel_err_hist
        ratio.GetXaxis().SetLimits(sum_hist.GetXaxis().GetXmin(), sum_hist.GetXaxis().GetXmax())
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
    
    if re.search("DiJet", stack_name):
        if re.search('_M', stack_name):
            ratio.GetXaxis().SetTitle("m_{DiJet} [GeV]")
        if re.search('pt', stack_name):
            ratio.GetXaxis().SetTitle("p_{T}^{DiJet} [GeV]")
        if re.search('eta', stack_name):
            ratio.GetXaxis().SetTitle("#eta_{DiJet}")
        if re.search('phi', stack_name):
            ratio.GetXaxis().SetTitle("#phi_{DiJet}")
    elif re.search("DiMuon", stack_name):
        if re.search('_M', stack_name):
            ratio.GetXaxis().SetTitle("m_{DiMuon} [GeV]")
        if re.search('pt', stack_name):
            ratio.GetXaxis().SetTitle("p_{T}^{DiMuon} [GeV]")
        if re.search('eta', stack_name):
            ratio.GetXaxis().SetTitle("#eta_{DiMuon}")
        if re.search('phi', stack_name):
            ratio.GetXaxis().SetTitle("#phi_{DiMuon}")
    else:
        if re.search('_M', stack_name):
            ratio.GetXaxis().SetTitle("m [GeV]")
        if re.search('pt', stack_name):
            ratio.GetXaxis().SetTitle("p_{T} [GeV]")
        if re.search('eta', stack_name):
            ratio.GetXaxis().SetTitle("#eta")
        if re.search('phi', stack_name):
            ratio.GetXaxis().SetTitle("#phi")
    c2.SaveAs("Stacks/stack_{}.pdf".format(stack_name))
