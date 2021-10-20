import ROOT
import plotHelper


def getMcData(kinematic: str, phyObj: str):
	zh = ROOT.TFile("./SBcategorizedTree/zh.root", "read")
	zjets = ROOT.TFile("./SBcategorizedTree/zjets.root", "read")
	tt = ROOT.TFile("./SBcategorizedTree/tt.root", "read")
	st = ROOT.TFile("./SBcategorizedTree/st.root", "read")
	qcd = ROOT.TFile("./SBcategorizedTree/qcd.root", "read")
	zz = ROOT.TFile("./SBcategorizedTree/zz.root", "read")
	data = ROOT.TFile("./SBcategorizedTree/data.root", "read")

	zhH = zh.Get("zh{}{}".format(phyObj, kinematic))
	zjetsH = zjets.Get("zjets{}{}".format(phyObj, kinematic))
	ttH = tt.Get("tt{}{}".format(phyObj, kinematic))
	stH = st.Get("st{}{}".format(phyObj, kinematic))
	qcdH = qcd.Get("qcd{}{}".format(phyObj, kinematic))
	zzH = zz.Get("zz{}{}".format(phyObj, kinematic))
	dataH = data.Get("data{}{}".format(phyObj, kinematic))

	plotHelper.plot_ratio("mcData", "mcData_{}_{}".format(phyObj, kinematic), zhH, stH, ttH, zzH, qcdH, zjetsH, dataH)

def getSRSB(kinematic: str, phyObj: str):
	zh = ROOT.TFile("./SRcategorizedTree/zh.root", "read")
	zjets = ROOT.TFile("./SRcategorizedTree/zjets.root", "read")
	tt = ROOT.TFile("./SRcategorizedTree/tt.root", "read")
	st = ROOT.TFile("./SRcategorizedTree/st.root", "read")
	qcd = ROOT.TFile("./SRcategorizedTree/qcd.root", "read")
	zz = ROOT.TFile("./SRcategorizedTree/zz.root", "read")

	zhSB = ROOT.TFile("./SBcategorizedTree/zh.root", "read")
	zjetsSB = ROOT.TFile("./SBcategorizedTree/zjets.root", "read")
	ttSB = ROOT.TFile("./SBcategorizedTree/tt.root", "read")
	stSB = ROOT.TFile("./SBcategorizedTree/st.root", "read")
	qcdSB= ROOT.TFile("./SBcategorizedTree/qcd.root", "read")
	zzSB = ROOT.TFile("./SBcategorizedTree/zz.root", "read")

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

	plotHelper.plot_ratio("srSideband", "srSideband_{}_{}".format(phyObj, kinematic), zhH, stH, ttH, zzH, qcdH, zjetsH, sumH)

kinematicList = ["Mass", "Pt", "Eta", "Phi"]
phyObjList = ["Z", "Higgs"]
for k in kinematicList:
	for p in phyObjList:
		getMcData(k, p)
		getSRSB(k, p)