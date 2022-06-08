from tkinter.messagebox import NO
import ROOT
import glob

def randomSelect(fileName: str) -> None:
	d = ROOT.RDataFrame("demo/dyTree", fileName)
	#print(d.Count().GetValue())
	dSkim = d.Range(0, d.Count().GetValue(), 50).Filter("z_mass_no_roccor >= 75 && z_mass_no_roccor <= 105").Filter("z_mass_roccor >= 75 && z_mass_no_roccor <= 105")
	dSkim.Snapshot("dyTree", "{}Skim.root".format(fileName.rstrip(".root")), d.GetColumnNames())


fileList = glob.glob("DYTreeNoBCut*.root")
for f in fileList:
	randomSelect(f)