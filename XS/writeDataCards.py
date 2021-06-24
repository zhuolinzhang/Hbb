import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", help="input root file name")
parser.add_argument("-o", help="output datacards path")
args = parser.parse_args()

sigHist = ROOT.TH1F()
bkgHist = ROOT.TH1F()
f = ROOT.TFile(args.n, "read")
sigHist = f.Get("sigHist")
bkgHist = f.Get("sumBkgHist")

for i in range(1, sigHist.GetNbinsX()):
	mass = sigHist.GetBinCenter(i)
	bkgBinNum = bkgHist.FindBin(mass)
	sigN = sigHist.GetBinContent(i)
	bkgN = bkgHist.GetBinContent(bkgBinNum)
	obs = sigN + bkgN
	with open(args.o + "/dataCard_mH{}.txt".format(mass), 'w') as ftxt:
		ftxt.write("imax    1 number of bins\n")
		ftxt.write("jmax    1 number of processes minus 1\n")
		ftxt.write("kmax    * number of nuisance parameters\n")
		ftxt.write("-" * 50 + "\n")
		ftxt.write("-" * 50 + "\n")
		ftxt.write("bin          signal_region\n")
		ftxt.write("observation  {}\n".format(obs))
		ftxt.write("-" * 50 + "\n")
		ftxt.write("bin\t\tsignal_region\tsignal_region\n")
		ftxt.write("process\t\tsignal\tbkg\n")
		ftxt.write("process\t\t0\t1\n")
		ftxt.write("rate\t\t{}\t{}\n".format(sigN, bkgN))
		ftxt.write("-" * 50 + "\n")
		ftxt.write("lumi13TeV_2018\tlnN\t1.023\t1.023\n")
		ftxt.write("BR_hbb\tlnN\t1.005\t-\n")
		ftxt.write("pdf_Higgs_qqbar\tlnN\t1.01\t-\n")
		ftxt.write("* autoMCStats 0\n")
