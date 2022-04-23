import ROOT
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-sf', help="Type of SFs, ID or ISO")
args = parser.parse_args()

histDict = {"ID": "NUM_LooseID_DEN_TrackerMuons_abseta_pt", "ISO": "NUM_LooseRelIso_DEN_LooseID_abseta_pt"}

rootFileList = glob.glob("MuonPOGSF/*UL_*{}.root".format(args.sf))
for file in rootFileList:
	fileName = file.split('/')[-1]
	f = ROOT.TFile(file, "read")
	c = ROOT.TCanvas()
	hist = ROOT.TH2F()
	hist = f.Get(histDict[args.sf])
	hist.SetTitle("")
	hist.GetXaxis().SetLabelSize(0.05)
	hist.GetXaxis().SetTitleSize(0.05)
	hist.GetYaxis().SetLabelSize(0.05)
	hist.GetYaxis().SetTitleSize(0.05)
	hist.GetYaxis().SetTitleOffset(0.99)
	hist.GetYaxis().SetTitle("p_{T} [GeV]")
	hist.GetZaxis().SetLabelSize(0.04)
	hist.GetZaxis().SetTitle("")
	c.SetRightMargin(0.13)
	hist.SetStats(0)
	ROOT.gStyle.SetPaintTextFormat("4.2e")
	hist.Draw("text e colz")

	c.SaveAs("MuonPOGSF/officialSFTh2/AppxB_{}.pdf".format(fileName.rstrip(".root")))