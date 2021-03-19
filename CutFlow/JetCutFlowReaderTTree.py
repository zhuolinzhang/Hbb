import ROOT
import json
import re
import sys
import os

sys.path.append("./lib")
import Plot
import FileIO

def setHistStyle(hist, color, legend, legend_title):
    hist.SetLineColor(color)
    legend.AddEntry(hist, legend_title, "l")
    if re.search("NoCut",hist.GetName()):
        hist.GetYaxis().SetTitle("Events / 2 GeV")
        hist.SetLineWidth(2)
        hist.SetLineStyle(2)
        hist.GetXaxis().SetTitle("m_{DiJet}")
        hist.Draw("HIST")
    else:
        hist.SetLineWidth(2)
        hist.Draw("HIST SAME")

if not(os.path.exists("CutFlowOutput")):
    os.mkdir("CutFlowOutput")

MCInfoList = []
factor = 1
cutFlowList = ["RecDiJet_NoCut", "RecDiJet_HMass", "RecDiJet_ptCut", "RecDiJet_JetID", "RecDiJet_btag"]
matchDict = {'ZH_HToBB':'sig', 'TTTo':'tt', 'channel':'st', 'ZZ':'dib', 'QCD':'qcd', 'DYJetsToLL':'zjets'}
legendDict = {"RecDiJet_NoCut": "No cut-off", "RecDiJet_HMass": "Higgs mass window", "RecDiJet_ptCut": "pt > 20 GeV", "RecDiJet_JetID": "JetID 2018", "RecDiJet_btag": "deepCSV"}
colorDict = {"RecDiJet_NoCut": ROOT.kRed, "RecDiJet_HMass": ROOT.kBlue, "RecDiJet_ptCut": ROOT.kGreen + 1, "RecDiJet_JetID": ROOT.kViolet - 2, "RecDiJet_btag": ROOT.kYellow + 1}
jetColl = ROOT.TTree()
'''
noCut_ = ROOT.TCut("jetNoCut == 1")
hMassCut_ = ROOT.TCut("hMassCut == 1") # change this after 2nd run
jetPtCut_ = ROOT.TCut("jetPtCut == 1")
jetIDCut_ = ROOT.TCut("jetID == 1")
btagCut_ = ROOT.TCut("btagCut == 1")
cutDict = {"RecDiJet_NoCut": "noCut_", "RecDiJet_HMass": "noCut_ && hMassCut_", "RecDiJet_ptCut": "noCut_ && hMassCut_ && jetPtCut_", "RecDiJet_JetID": "noCut_ && hMassCut_ && jetPtCut_ && jetIDCut_", "RecDiJet_btag": "noCut_ && hMassCut_ && jetPtCut_ && jetIDCut_ && btagCut_"}
'''
cutDict = {"RecDiJet_NoCut": "jetNoCut == 1", "RecDiJet_HMass": "jetNoCut == 1 && hMassCut == 1", "RecDiJet_ptCut": "jetNoCut == 1 && hMassCut == 1 && jetPtCut == 1", "RecDiJet_JetID": "jetNoCut == 1 && hMassCut == 1 && jetPtCut == 1 && jetID == 1", "RecDiJet_btag": "jetNoCut == 1 && hMassCut == 1 && jetPtCut == 1 && jetID == 1 && btag == 1"}

for i in matchDict.values():
    for j in cutFlowList:
        exec('{0}_{1}_M = ROOT.TH1F("{0}_{1}_M", "", 75, 50, 200)'.format(i, j))

with open("./MCInfo.json") as MCInfo:
    MCInfoList = json.load(MCInfo)

for i in matchDict.values():
    for j in cutFlowList:
        exec("{0}_{1}_M_N = 0.".format(i, j))

MCSampleList = FileIO.open_file("./Sample") # path
for rootFile in MCSampleList:
    jetColl = rootFile.Get("demo/jetColl")
    compareName = FileIO.get_primary_name(MCSampleList.index(rootFile), "./Sample")
    # Read scale factor and check the factor for each dataset is right
    for i in MCInfoList:
        for key, value in i.items():
            if key == 'primary_name':
                if value == compareName:
                    factor = i['factor_2018']
                    factor = factor * 0.004536324
                    print("The primary name: ", value)
                    print("The factor is ", factor)
                    break
    
    for s in cutFlowList:
        exec('jetColl.Draw("higgsMass >> h_{}_M(75, 50, 200)", "{}")'.format(s, cutDict[s])) # change this !!!!!!!!!!!!!!!!!!!!
        exec('h_{0}_M = ROOT.gROOT.FindObject("h_{0}_M")'.format(s))
    # Scale histograms, the scale factor is from MCInfo.json
    for s in cutFlowList:
        exec("Plot.scale_hist(h_{}_M, factor)".format(s))
        exec("h_{}_M_N = jetColl.GetEntries('{}') * factor".format(s, cutDict[s]))
    # Categorize MC samples
    for s in cutFlowList:
        for key, value in matchDict.items():
            if re.search(key, compareName):
                exec("{0}_{1}_M += h_{1}_M".format(value, s)) # e.g. sig_RecDiJet_Trigger_M
                exec("{0}_{1}_M_N += h_{1}_M_N".format(value, s))

# Write cutflow tables
for i in matchDict.values():
    exec("noCutN = {}_RecDiJet_NoCut_M_N".format(i))
    with open("JetCutFlowOutput/{}.txt".format(i), 'w') as outputTable:
        for j in cutFlowList:
            exec("{1}_eff = {0}_{1}_M_N / noCutN * 100".format(i, j))
            exec("outputTable.write('{0}_{1} \t')".format(i, j))
            exec("outputTable.write('%.3f \\t' % {}_{}_M_N)".format(i, j))
            exec("outputTable.write('%.4f' % {}_eff + '%' + '\\n')".format(j))

# Plot invariant mass spectrum
for i in matchDict.values():
    c = ROOT.TCanvas()
    c.SetLogy()
    c.Draw()
    ROOT.gStyle.SetOptStat(ROOT.kFALSE)
    l = ROOT.TLegend(.7, .7, .9, .9)
    for j in cutFlowList:
        exec("setHistStyle({0}_{1}_M, colorDict['{1}'], l, legendDict['{1}'])".format(i, j))
    exec("{}_RecDiJet_NoCut_M.SetMaximum(1e5)".format(i))
    exec("{}_RecDiJet_NoCut_M.SetMinimum(1e-3)".format(i))
    l.Draw()
    c.SaveAs("JetCutFlowOutput/cutflow_{}.pdf".format(i))
