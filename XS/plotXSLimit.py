import ROOT
import numpy as np
import glob
import argparse
import uproot

ROOT.gROOT.SetBatch()

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="The folder of results")
parser.add_argument("-y", default="run2", help="The year of datasets")
args = parser.parse_args()

xsLimitExpected = np.array([], 'd')
xsLimitExpected95up = np.array([], 'd')
xsLimitExpected95down = np.array([], 'd')
xsLimitExpected68up = np.array([], 'd')
xsLimitExpected68down = np.array([], 'd')
xsLimitObserved = np.array([], 'd')
signalStrengthLimitExpected = np.array([], 'd')
signalStrengthLimitExpected95up = np.array([], 'd')
signalStrengthLimitExpected95down = np.array([], 'd')
signalStrengthLimitExpected68up = np.array([], 'd')
signalStrengthLimitExpected68down = np.array([], 'd')
signalStrengthLimitObserved = np.array([], 'd')
mass = np.array([], 'd')
masserr = np.array([], 'd')
expectedYErr = np.array([], 'd') # a np.zero array

# make the loop
xsFile = uproot.open('./smXS/HiggsXS.root')
massTotal = xsFile['genHiggsXS'].axis().centers()
massErrTotal = xsFile['genHiggsXS'].axis().widths()
xsList = xsFile['genHiggsXS'].values()

label = 'p_{T}(H)'
rootFileList = glob.glob("./{}/*.root".format(args.f))
fileList = []
for i in rootFileList:
	f = ROOT.TFile("./{}".format(i))
	t = f.Get("limit")
	if not t: continue
	if t.GetEntries() == 2: continue
	fileList.append(i)

for i in fileList:
	m = massTotal[fileList.index(i)]
	f = ROOT.TFile("./{}/higgsCombine.test.pt{:.1f}.AsymptoticLimits.mH125.root".format(args.f, m))
	# f = ROOT.TFile("./DijetPtResult/higgsCombinetest.AsymptoticLimits.mH{}.root".format(m))
	tree = f.Get("limit")
	tree.GetEntry(2)
	xsLimitExpected = np.append(xsLimitExpected, tree.limit * xsList[fileList.index(i)])
	signalStrengthLimitExpected = np.append(signalStrengthLimitExpected, tree.limit)

	tree = f.Get("limit")
	tree.GetEntry(0)
	xsLimitExpected95up = np.append(xsLimitExpected95up, abs(tree.limit - signalStrengthLimitExpected[fileList.index(i)]) * xsList[fileList.index(i)])
	signalStrengthLimitExpected95up = np.append(signalStrengthLimitExpected95up, abs(tree.limit - signalStrengthLimitExpected[fileList.index(i)]))

	tree = f.Get("limit")
	tree.GetEntry(4)
	xsLimitExpected95down = np.append(xsLimitExpected95down, abs(tree.limit - signalStrengthLimitExpected[fileList.index(i)]) * xsList[fileList.index(i)])
	signalStrengthLimitExpected95down = np.append(signalStrengthLimitExpected95down, abs(tree.limit - signalStrengthLimitExpected[fileList.index(i)]))
	
	tree.GetEntry(1)
	xsLimitExpected68up = np.append(xsLimitExpected68up, abs(tree.limit - signalStrengthLimitExpected[fileList.index(i)]) * xsList[fileList.index(i)])
	signalStrengthLimitExpected68up = np.append(signalStrengthLimitExpected68up, abs(tree.limit - signalStrengthLimitExpected[fileList.index(i)]))
	tree = f.Get("limit")

	tree.GetEntry(3)
	xsLimitExpected68down = np.append(xsLimitExpected68down, abs(tree.limit - signalStrengthLimitExpected[fileList.index(i)]) * xsList[fileList.index(i)])
	signalStrengthLimitExpected68down = np.append(signalStrengthLimitExpected68down, abs(tree.limit - signalStrengthLimitExpected[fileList.index(i)]))
	
	tree.GetEntry(5)
	xsLimitObserved = np.append(xsLimitObserved, tree.limit * xsList[fileList.index(i)])
		
	mass = np.append(mass, m) # use this to avoid TGraph definition error
	masserr = np.append(masserr, massErrTotal[fileList.index(i)])
	expectedYErr = np.append(expectedYErr, 0.)
	
c1=ROOT.TCanvas("c1", "c1", 800, 600)
c1.SetBottomMargin(.15)
c1.SetLeftMargin(.15)
#c1.SetGrid()
c1.SetLogy()
#c1.SetLogx()

masserr = masserr / 2
mgXS = ROOT.TMultiGraph()
mgSignalStrength = ROOT.TMultiGraph()
graphXSLimitExpected = ROOT.TGraphErrors(len(mass), mass, xsLimitExpected, masserr, expectedYErr)
#graphXSLimitExpected.SetMarkerSize(1)
#graphXSLimitExpected.SetMarkerStyle(20)
graphXSLimitExpected.SetMarkerColor(ROOT.kGreen + 1)
graphXSLimitExpected.SetLineWidth(2)
graphXSLimitExpected.SetLineStyle(7)

'''
graph_limitObserved = ROOT.TGraph(len(mass), mass, limitObserved)
graph_limitObserved.SetMarkerStyle(20)
'''

graphXSLimit95up = ROOT.TGraphAsymmErrors(len( mass), mass, xsLimitExpected, masserr, masserr, xsLimitExpected95up, xsLimitExpected95down)
graphXSLimit95up.SetTitle("graph_limit95up")
graphXSLimit95up.SetFillColor(ROOT.kOrange)

graphXSLimit68up = ROOT.TGraphAsymmErrors(len( mass), mass, xsLimitExpected, masserr, masserr, xsLimitExpected68up, xsLimitExpected68down)
graphXSLimit68up.SetTitle("graph_limit68up")
graphXSLimit68up.SetFillColor(ROOT.kGreen + 1)


graphSignalStrengthLimitExpected = ROOT.TGraphErrors(len(mass), mass, signalStrengthLimitExpected, masserr, expectedYErr)
#graphSignalStrengthLimitExpected.SetMarkerSize(0)
#graphSignalStrengthLimitExpected.SetMarkerStyle(20)
#graphSignalStrengthLimitExpected.SetMarkerColor(ROOT.kGreen + 1)
graphSignalStrengthLimitExpected.SetLineWidth(2)
graphSignalStrengthLimitExpected.SetLineStyle(7)

'''
graphSignalStrengthimitObserved = ROOT.TGraph(len(mass), mass, limitObserved)
graphSignalStrengthimitObserved.SetMarkerStyle(20)
'''

graphSignalStrengthLimit95up = ROOT.TGraphAsymmErrors(len( mass), mass, signalStrengthLimitExpected, masserr, masserr, signalStrengthLimitExpected95up, signalStrengthLimitExpected95down)
graphSignalStrengthLimit95up.SetTitle("graph_limit95up")
graphSignalStrengthLimit95up.SetFillColor(ROOT.kOrange)

graphSignalStrengthLimit68up = ROOT.TGraphAsymmErrors(len( mass), mass, signalStrengthLimitExpected, masserr, masserr, signalStrengthLimitExpected68up, signalStrengthLimitExpected68down)
graphSignalStrengthLimit68up.SetTitle("graph_limit68up")
graphSignalStrengthLimit68up.SetFillColor(ROOT.kGreen + 1)

mgXS.Add(graphXSLimit95up, "2")
mgXS.Add(graphXSLimit68up, "2")
mgXS.Add(graphXSLimitExpected, "Z")
#mgXS.Add(graph_limitObserved, "pl")

mgXS.Draw("A")

#mgXS.GetYaxis().SetTitle(
#	"#sigma(pp#rightarrow ZH)#times BR(Z#rightarrow #mu#mu)#times BR(H#rightarrow b#bar{b}). [pb]")
mgXS.GetYaxis().SetTitle("95% CL Limit on d#sigma(ZH)#timesBR(H#rightarrowb#bar{b} / dp_{T} [fb/ N GeV]")
mgXS.GetYaxis().SetTitleSize(0.04)
mgXS.GetXaxis().SetTitle("{} [GeV]".format(label))
mgXS.GetXaxis().SetTitleSize(0.05)
mgXS.GetYaxis().SetTitleOffset(1.0)
mgXS.GetXaxis().SetRangeUser(mass[0] - masserr[0], mass[-1] + masserr[-1])

c1.Update()
legend = ROOT.TLegend(0.5, 0.6, 0.8, 0.9)
cmsTag = ROOT.TLatex(0.13, 0.917, "#scale[1.1]{CMS}")
cmsTag.SetNDC()
cmsTag.SetTextAlign(11)
cmsTag.Draw()
cmsTag2 = ROOT.TLatex(0.215, 0.917, "#scale[0.825]{#bf{#it{Work in progress}}}")
cmsTag2.SetNDC()
cmsTag2.SetTextAlign(11)
#cmsTag.SetTextFont(61)
cmsTag2.Draw()

#labelDict = {"run2": "#scale[0.9]{#bf{137.64 fb^{-1} (13 TeV, Run 2)}}", "2018": "#scale[0.9]{#bf{59.83 fb^{-1} (13 TeV, 2018)}}", "2017": "#scale[0.9]{#bf{41.48 fb^{-1} (13 TeV, 2017)}}", "2016": "#scale[0.9]{#bf{16.81 fb^{-1} (13 TeV, 2016)}}", "2016APV": "#scale[0.9]{#bf{19.52 fb^{-1} (13 TeV, 2016APV)}}"}
labelDict = {"run2": "#scale[0.9]{#bf{137.64 fb^{-1} (13 TeV, Run 2)}}", "2018": "#scale[0.9]{#bf{59.83 fb^{-1} (13 TeV, 2018)}}",
        "2017": "#scale[0.9]{#bf{41.48 fb^{-1} (13 TeV, 2017)}}", "2016": "#scale[0.9]{#bf{36.33 fb^{-1} (13 TeV, 2016)}}", "2016APV": "#scale[0.9]{#bf{19.52 fb^{-1} (13 TeV, 2016APV)}}"}
cmsTag3 = ROOT.TLatex(0.90, 0.917, "{}".format(labelDict[args.y]))
cmsTag3.SetNDC()
cmsTag3.SetTextAlign(31)
#cmsTag.SetTextFont(61)
cmsTag3.Draw()

xsLine10to20 = ROOT.TArrow(60, 0, 60, 10, 0.02, "<|")
xsLine20to50 = ROOT.TArrow(300, 0, 300, 10, 0.02, "<|")
xsLine50to100 = ROOT.TArrow(400, 0, 400, 10, 0.02, "<|")
xsLine10to20.SetLineWidth(2)
xsLine20to50.SetLineWidth(2)
xsLine50to100.SetLineWidth(2)
#xsLine10to20.Draw()
#xsLine20to50.Draw()
#xsLine50to100.Draw()

leg1 = ROOT.TLegend(0.65, 0.65, 0.88, 0.85)  
leg1.SetBorderSize(0)
leg1.SetFillStyle(1001)
leg1.SetFillColor(ROOT.kWhite) 

leg1.AddEntry(graphXSLimitExpected, "Expected",  "PL")
leg1.AddEntry(graphXSLimit68up, "68% Expected",  "F")
leg1.AddEntry(graphXSLimit95up, "95% Expected",  "F")
leg1.Draw("same")

c1.SaveAs("xs_pt_{}.pdf".format(args.y))

c2 = ROOT.TCanvas("c2", "c2", 800, 600)
c2.SetBottomMargin(.15)

mgSignalStrength.Add(graphSignalStrengthLimit95up, "2")
mgSignalStrength.Add(graphSignalStrengthLimit68up, "2")
mgSignalStrength.Add(graphSignalStrengthLimitExpected, "Z")

sumExpectedUpperLimits = signalStrengthLimitExpected + signalStrengthLimitExpected95up + signalStrengthLimitExpected68up
upperRangeInYaxis = np.amax(sumExpectedUpperLimits) * 1.2
mgSignalStrength.GetYaxis().SetRangeUser(0, upperRangeInYaxis) # Set range of Y axis in the signal strength distribution
mgSignalStrength.GetYaxis().SetTitle("95% CL Limit on Signal Strength")
mgSignalStrength.GetYaxis().SetTitleSize(0.05)
mgSignalStrength.GetXaxis().SetTitle("{} [GeV]".format(label))
mgSignalStrength.GetXaxis().SetTitleSize(0.05)
mgSignalStrength.GetYaxis().SetTitleOffset(1.0)
mgSignalStrength.GetXaxis().SetRangeUser(mass[0] - masserr[0], mass[-1] + masserr[-1])
mgSignalStrength.Draw("A")
cmsTag.Draw()
cmsTag2.Draw()
cmsTag3.Draw()

#leg2 = ROOT.TLegend(0.15, 0.65, 0.38, 0.85) 
#leg2 = ROOT.TLegend(0.65, 0.65, 0.88, 0.85) # legend of signal strength distribution  
leg2 = ROOT.TLegend(0.45, 0.65, 0.65, 0.85) # legend of signal strength distribution  
leg2.SetBorderSize(0)
leg2.SetFillStyle(1001)
leg2.SetFillColor(ROOT.kWhite) 
leg2.AddEntry(graphSignalStrengthLimitExpected, "Expected",  "L")
leg2.AddEntry(graphSignalStrengthLimit68up, "68% Expected",  "F")
leg2.AddEntry(graphSignalStrengthLimit95up, "95% Expected",  "F")
leg2.Draw("same")
signalStrengthLine10to20 = ROOT.TArrow(60, 0.01, 60, 10, 0.02, "<|")
signalStrengthLine20to50 = ROOT.TArrow(300, 0.01, 300, 10, 0.02, "<|")
signalStrengthLine50to100 = ROOT.TArrow(400, 0.01, 400, 10, 0.02, "<|")
signalStrengthLine10to20.SetLineWidth(2)
signalStrengthLine20to50.SetLineWidth(2)
signalStrengthLine50to100.SetLineWidth(2)
#signalStrengthLine10to20.Draw()
#signalStrengthLine20to50.Draw()
#signalStrengthLine50to100.Draw()
c2.SaveAs("signal_strength_pt_{}.pdf".format(args.y))
# Calculate the total distribution
print("The total XS is {}".format(np.sum(xsLimitExpected)))