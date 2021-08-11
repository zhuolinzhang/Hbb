import ROOT
import numpy as np
import glob
import argparse
import uproot

ROOT.gROOT.SetBatch()

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", help="m or pt")
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
lable = ''

# make the loop
xsFile = uproot.open('./smXS/HiggsXS.root')
massTotal = xsFile['recoHiggsXS'].axis().centers()
xsList = xsFile['recoHiggsXS'].values()

if args.type == 'm':
	lable = 'm_{Dijet}'
elif args.type == 'pt':
	lable = 'p_{T}^{Dijet}'
rootFileList = glob.glob("./DijetPtResult/*.root")
fileList = []
for i in rootFileList:
	f = ROOT.TFile("./{}".format(i))
	t = f.Get("limit")
	if not t: continue
	if t.GetEntries() == 2: continue
	fileList.append(i)

for i in fileList:
	m = massTotal[fileList.index(i)]
	f = ROOT.TFile("./DijetPtResult/higgsCombine.test.pt{}.AsymptoticLimits.mH125.root".format(m))
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
		
	mass = np.append(mass, m)
	masserr = np.append(masserr, 0.)
	
c1=ROOT.TCanvas("c1", "c1", 800, 600)
c1.SetBottomMargin(.15)
c1.SetLeftMargin(.15)
#c1.SetGrid()
c1.SetLogy()
#c1.SetLogx()

mgXS = ROOT.TMultiGraph()
mgSignalStrength = ROOT.TMultiGraph()
mgeps = ROOT.TMultiGraph()

graphXSLimitExpected = ROOT.TGraph(len(mass), mass, xsLimitExpected)
graphXSLimitExpected.SetMarkerSize(1)
graphXSLimitExpected.SetMarkerStyle(20)
graphXSLimitExpected.SetMarkerColor(ROOT.kBlack)
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


graphSignalStrengthLimitExpected = ROOT.TGraph(len(mass), mass, signalStrengthLimitExpected)
graphSignalStrengthLimitExpected.SetMarkerSize(1)
graphSignalStrengthLimitExpected.SetMarkerStyle(20)
graphSignalStrengthLimitExpected.SetMarkerColor(ROOT.kBlack)
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

mgXS.Add(graphXSLimit95up, "3")
mgXS.Add(graphXSLimit68up, "3")
mgXS.Add(graphXSLimitExpected, "pl")
#mgXS.Add(graph_limitObserved, "pl")

mgSignalStrength.Add(graphSignalStrengthLimit95up, "3")
mgSignalStrength.Add(graphSignalStrengthLimit68up, "3")
mgSignalStrength.Add(graphSignalStrengthLimitExpected, "pl")

mgXS.Draw("APC")

#mgXS.GetYaxis().SetTitle(
#	"#sigma(pp#rightarrow ZH)#times BR(Z#rightarrow #mu#mu)#times BR(H#rightarrow b#bar{b}). [pb]")
mgXS.GetYaxis().SetTitle("d#sigma(ZH)#timesBR(Z#rightarrowl^{+}l^{-}) / dp_{T} [fb/ N GeV]")
mgXS.GetYaxis().SetTitleSize(0.05)
mgXS.GetXaxis().SetTitle("{}[GeV]".format(lable))
mgXS.GetXaxis().SetTitleSize(0.05)
mgXS.GetYaxis().SetTitleOffset(1.0)
mgXS.GetXaxis().SetRangeUser(mass[0] - 1, mass[-1] + .1)

c1.Update()
legend = ROOT.TLegend(0.5, 0.6, 0.8, 0.9)
cmsTag = ROOT.TLatex(0.13, 0.917, "#scale[1.1]{CMS}")
cmsTag.SetNDC()
cmsTag.SetTextAlign(11)
cmsTag.Draw()
cmsTag2 = ROOT.TLatex(0.215, 0.917, "#scale[0.825]{#bf{#it{Preliminary}}}")
cmsTag2.SetNDC()
cmsTag2.SetTextAlign(11)
#cmsTag.SetTextFont(61)
cmsTag2.Draw()
cmsTag3 = ROOT.TLatex(
	0.90, 0.917, "#scale[0.9]{#bf{59.83 fb^{-1} (13 TeV, 2018)}}")
cmsTag3.SetNDC()
cmsTag3.SetTextAlign(31)
#cmsTag.SetTextFont(61)
cmsTag3.Draw()
leg1 = ROOT.TLegend(0.65, 0.65, 0.88, 0.85)  
leg1.SetBorderSize(0)
leg1.SetFillStyle(1001)
leg1.SetFillColor(ROOT.kWhite) 

leg1.AddEntry(graphXSLimitExpected, "Expected",  "PL")
leg1.AddEntry(graphXSLimit68up, "68% Expected",  "F")
leg1.AddEntry(graphXSLimit95up, "95% Expected",  "F")
leg1.Draw("same")
c1.SaveAs("xs_{}.pdf".format(args.type))

c2 = ROOT.TCanvas()
mgSignalStrength.GetYaxis().SetTitle("Signal Strength")
mgSignalStrength.GetYaxis().SetTitleSize(0.05)
mgSignalStrength.GetXaxis().SetTitle("{}[GeV]".format(lable))
mgSignalStrength.GetXaxis().SetTitleSize(0.05)
mgSignalStrength.GetYaxis().SetTitleOffset(1.0)
mgSignalStrength.GetXaxis().SetRangeUser(mass[0] - 1, mass[-1] + .1)
mgSignalStrength.Draw("APC")
cmsTag.Draw()
cmsTag2.Draw()
cmsTag3.Draw()
leg2 = ROOT.TLegend(0.15, 0.65, 0.38, 0.85)  
leg2.SetBorderSize(0)
leg2.SetFillStyle(1001)
leg2.SetFillColor(ROOT.kWhite) 
leg2.AddEntry(graphSignalStrengthLimitExpected, "Expected",  "PL")
leg2.AddEntry(graphSignalStrengthLimit68up, "68% Expected",  "F")
leg2.AddEntry(graphSignalStrengthLimit95up, "95% Expected",  "F")
leg2.Draw("same")
c2.SaveAs("signalStrength_{}.pdf".format(args.type))
# Calculate the total distribution
print("The total XS is {}".format(np.sum(xsLimitExpected)))