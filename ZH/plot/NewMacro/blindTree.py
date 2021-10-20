import ROOT
import argparse

def cutTree(treeName: str, fileName: str, sbPath: str, srPath: str) -> None:
	# add check output path funciton here!!!
	ROOT.ROOT.EnableImplicitMT()
	print("Read {}".format(fileName))
	exitFlag = False
	d = ROOT.RDataFrame(treeName, fileName)
	if d.Count().GetValue() == 0: exitFlag = True
	if not exitFlag:
		dSideBand = d.Filter("higgs_mass < 90 || higgs_mass > 150")
		branchList = d.GetColumnNames()
		dSideBand.Snapshot("ZHCandidates", sbPath, branchList)
		if "DoubleMuon" in fileName: pass
		else:
			dSR = d.Filter("higgs_mass >= 90 && higgs_mass <= 150")
			dSR.Snapshot("ZHCandidates", srPath, branchList)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", help="The path of input .root file")
	parser.add_argument("-sr", help="The path of output signal region .root file")
	parser.add_argument("-sb", help="The path of output sideband .root file")
	parser.add_argument("-t", default="ZHCandidates", help="The name of TTree which you want to blind")
	args = parser.parse_args()
	cutTree(args.t, args.i, args.sr, args.sb)