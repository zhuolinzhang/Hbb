import ROOT
from array import array
import glob
import argparse

ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument("--type", help="m or pt")
args = parser.parse_args()

limitExpected = array('d')
limitExpected95up = array('d')
limitExpected95down = array('d')
limitExpected68up = array('d')
limitExpected68down = array('d')
limitObserved = array('d')
mass = array('d')
masserr = array('d')
lable = ''

#make the loop
if args.type == 'm':
	massTotal = list(range(51, 91, 2)) + list(range(151, 199, 2))
	lable = 'm_{Dijet}'
elif args.type == 'pt':
	massTotal = list(range(5, 490, 10))
	lable = 'p_{T}^{Dijet}'
rootFileList = glob.glob("*.root")
fileList = []
for i in rootFileList:
	f = ROOT.TFile("./{}".format(i))
	t = f.Get("limit")
	if not t: continue
	if t.GetEntries() == 2: continue
	fileList.append(i)

for i in fileList:
	m = massTotal[fileList.index(i)]
	f = ROOT.TFile("./higgsCombinetest.AsymptoticLimits.mH{}.root".format(m))
	tree = f.Get("limit")
	tree.GetEntry(2)
	limitExpected.append(tree.limit)

	tree = f.Get("limit")
	tree.GetEntry(0)
	limitExpected95up.append(abs(tree.limit - limitExpected[-1]))
	tree = f.Get("limit")
	tree.GetEntry(4)
	limitExpected95down.append(abs(tree.limit - limitExpected[-1]))
	
	tree.GetEntry(1)
	limitExpected68up.append(abs(tree.limit - limitExpected[-1]))
	tree = f.Get("limit")
	tree.GetEntry(3)
	limitExpected68down.append(abs(tree.limit - limitExpected[-1]))
	
	tree.GetEntry(5)
	limitObserved.append(tree.limit)
		
	mass.append(m)
	masserr.append(0.)
	
c1=ROOT.TCanvas("c1","c1",700,500)
#c1.SetGrid()
#c1.SetLogy()
#c1.SetLogx()

mg=ROOT.TMultiGraph()
mgeps=ROOT.TMultiGraph()

graph_limitExpected = ROOT.TGraph(len(mass), mass, limitExpected)
graph_limitExpected.SetMarkerSize(1)
graph_limitExpected.SetMarkerStyle(20)
graph_limitExpected.SetMarkerColor(ROOT.kBlack)
graph_limitExpected.SetLineWidth(2)
graph_limitExpected.SetLineStyle(7)

'''
graph_limitObserved = ROOT.TGraph(len(mass), mass, limitObserved)
graph_limitObserved.SetMarkerStyle(20)
'''

graph_limit95up = ROOT.TGraphAsymmErrors(len(
	mass), mass, limitExpected, masserr, masserr, limitExpected95up, limitExpected95down)
graph_limit95up.SetTitle("graph_limit95up")
graph_limit95up.SetFillColor(ROOT.kOrange - 2)

graph_limit68up = ROOT.TGraphAsymmErrors(len(
	mass), mass, limitExpected, masserr, masserr, limitExpected68up, limitExpected68down)
graph_limit68up.SetTitle("graph_limit68up")
graph_limit68up.SetFillColor(ROOT.kGreen - 6)

mg.Add(graph_limit95up, "3")
mg.Add(graph_limit68up, "3")
mg.Add(graph_limitExpected, "pl")
#mg.Add(graph_limitObserved, "pl")

mg.Draw("APC")

#mg.GetYaxis().SetTitle(
#	"#sigma(pp#rightarrow ZH)#times BR(Z#rightarrow #mu#mu)#times BR(H#rightarrow b#bar{b}). [pb]")
mg.GetYaxis().SetTitle("Signal Strength")
mg.GetYaxis().SetTitleSize(0.05)
mg.GetXaxis().SetTitle("{}[GeV]".format(lable))
mg.GetXaxis().SetTitleSize(0.05)
mg.GetYaxis().SetTitleOffset(1.0)
mg.GetXaxis().SetRangeUser(mass[0] - .1, mass[-1] + .1)

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
	0.90, 0.917, "#scale[0.9]{#bf{0.271 fb^{-1} (13 TeV, 2018)}}")
cmsTag3.SetNDC()
cmsTag3.SetTextAlign(31)
#cmsTag.SetTextFont(61)
cmsTag3.Draw()
leg=ROOT.TLegend(0.65, 0.65,0.88, 0.85)  
leg.SetBorderSize(0)
leg.SetFillStyle(1001)
leg.SetFillColor(ROOT.kWhite) 

leg.AddEntry(graph_limitExpected, "Expected",  "PL")
leg.AddEntry(graph_limit68up, "68% Expected",  "F")
leg.AddEntry(graph_limit95up, "95% Expected",  "F")
leg.Draw("same")
c1.SaveAs("limit_{}.pdf".format(args.type))
