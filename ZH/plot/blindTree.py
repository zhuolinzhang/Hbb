import ROOT
import argparse

def cutTree(treeName: str, fileName: str, sbPath: str, sbPathForHiggsMass: str, srPath: str) -> None:
	ROOT.ROOT.EnableImplicitMT()
	print("Blind {}".format(fileName))
	try:
		exitFlag = False
		d = ROOT.RDataFrame(treeName, fileName)
		if d.Count().GetValue() == 0: exitFlag = True
		if not exitFlag:
			branchList = d.GetColumnNames()
			dSideBand = d.Filter("higgs_mass < 90 || higgs_mass > 150")
			if dSideBand.Count().GetValue() > 0:
				dSideBand.Snapshot("ZHCandidates", sbPath, branchList)
			if "DoubleMuon" in fileName:
				if dSideBand.Count().GetValue() > 0:
					dSideBand.Snapshot("ZHCandidates", sbPathForHiggsMass, ("z_mass", "higgs_mass"))
			else:
				d.Snapshot("ZHCandidates", sbPathForHiggsMass, ("z_mass", "higgs_mass", "z_sf"))
				dSR = d.Filter("higgs_mass >= 90 && higgs_mass <= 150")
				if dSR.Count().GetValue() > 0:
					dSR.Snapshot("ZHCandidates", srPath, branchList)
	except:
		print("This file {} is empty!".format(fileName))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", help="The path of input .root file")
	parser.add_argument("-sr", help="The path of output signal region .root file")
	parser.add_argument("-sb", help="The path of output sideband .root file")
	parser.add_argument("-sbHM", help="The path of output sideband .root file only for plotting Higgs mass")
	parser.add_argument("-t", default="ZHCandidates", help="The name of TTree which you want to blind")
	args = parser.parse_args()
	cutTree(args.t, args.i, args.sb, args.sbHM, args.sr)