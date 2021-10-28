import ROOT
import plotHelper
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-sbPath", default="SBcategorizedTree", help="The path of categorized sideband TTrees")
parse.add_argument("-srPath", default="SRcategorizedTree", help="The path of categorized signal region TTrees")
parse.add_argument("-y", default="run2", help="The year you want to plot")
args = parse.parse_args()

def getMcData(kinematic: str, phyObj: str, path: str) -> None:
	zh = ROOT.TFile("./{}/zh.root".format(path), "read")
	zjets = ROOT.TFile("./{}/zjets.root".format(path), "read")
	tt = ROOT.TFile("./{}/tt.root".format(path), "read")
	st = ROOT.TFile("./{}/st.root".format(path), "read")
	qcd = ROOT.TFile("./{}/qcd.root".format(path), "read")
	zz = ROOT.TFile("./{}/zz.root".format(path), "read")
	data = ROOT.TFile("./{}/data.root".format(path), "read")

	zhH = zh.Get("zh{}{}".format(phyObj, kinematic))
	zjetsH = zjets.Get("zjets{}{}".format(phyObj, kinematic))
	ttH = tt.Get("tt{}{}".format(phyObj, kinematic))
	stH = st.Get("st{}{}".format(phyObj, kinematic))
	qcdH = qcd.Get("qcd{}{}".format(phyObj, kinematic))
	zzH = zz.Get("zz{}{}".format(phyObj, kinematic))
	dataH = data.Get("data{}{}".format(phyObj, kinematic))

	if not qcdH:
		qcdH = ROOT.TH1D()
		qcdH.SetName("qcd{}{}".format(phyObj, kinematic))
	plotHelper.plot_ratio("mcData", "mcData_{}_{}".format(phyObj, kinematic), args.y, zhH, stH, ttH, zzH, qcdH, zjetsH, dataH)

def getSRSB(kinematic: str, phyObj: str, sbPath: str, srPath: str):
	zh = ROOT.TFile("./{}/zh.root".format(srPath), "read")
	zjets = ROOT.TFile("./{}/zjets.root".format(srPath), "read")
	tt = ROOT.TFile("./{}/tt.root".format(srPath), "read")
	st = ROOT.TFile("./{}/st.root".format(srPath), "read")
	qcd = ROOT.TFile("./{}/qcd.root".format(srPath), "read")
	zz = ROOT.TFile("./{}/zz.root".format(srPath), "read")

	zhSB = ROOT.TFile("./{}/zh.root".format(sbPath), "read")
	zjetsSB = ROOT.TFile("./{}/zjets.root".format(sbPath), "read")
	ttSB = ROOT.TFile("./{}/tt.root".format(sbPath), "read")
	stSB = ROOT.TFile("./{}/st.root".format(sbPath), "read")
	qcdSB= ROOT.TFile("./{}/qcd.root".format(sbPath), "read")
	zzSB = ROOT.TFile("./{}/zz.root".format(sbPath), "read")

	zhH = zh.Get("zh{}{}".format(phyObj, kinematic))
	zjetsH = zjets.Get("zjets{}{}".format(phyObj, kinematic))
	ttH = tt.Get("tt{}{}".format(phyObj, kinematic))
	stH = st.Get("st{}{}".format(phyObj, kinematic))
	qcdH = qcd.Get("qcd{}{}".format(phyObj, kinematic))
	zzH = zz.Get("zz{}{}".format(phyObj, kinematic))

	zhHSB = zhSB.Get("zh{}{}".format(phyObj, kinematic))
	zjetsHSB = zjetsSB.Get("zjets{}{}".format(phyObj, kinematic))
	ttHSB = ttSB.Get("tt{}{}".format(phyObj, kinematic))
	stHSB = stSB.Get("st{}{}".format(phyObj, kinematic))
	qcdHSB = qcdSB.Get("qcd{}{}".format(phyObj, kinematic))
	zzHSB = zzSB.Get("zz{}{}".format(phyObj, kinematic))
	sumH = zhHSB + zjetsHSB + ttHSB + stHSB + qcdHSB + zzHSB
	sumH.SetName("sumSideband")

	if not qcdH:
		plotHelper.plot_ratio("srSideband", "srSideband_{}_{}".format(phyObj, kinematic), args.y, zhH, stH, ttH, zzH, zjetsH, sumH)
	else:
		plotHelper.plot_ratio("srSideband", "srSideband_{}_{}".format(phyObj, kinematic), args.y, zhH, stH, ttH, zzH, qcdH, zjetsH, sumH)

kinematicList = ["Mass", "Pt", "Eta", "Phi"]
phyObjList = ["Z", "Higgs"]
for k in kinematicList:
	for p in phyObjList:
		getMcData(k, p, args.sbPath)
		getSRSB(k, p, args.sbPath, args.srPath)