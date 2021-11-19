import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="The name of input root file name w/o index number")
args = parser.parse_args()

def produceCondorScript(totalBinNum: int) -> None:
	with open("condor_fit_{}.sub".format(binNum), 'w') as fOut:
		fOut.write("executable = condor_fit_$(ProcId).sh\n".format(binNum))
		fOut.write("output                = $(ClusterId).$(ProcId).out\n")
		fOut.write("error                 = $(ClusterId).$(ProcId).err\n")
		fOut.write("log                   = $(ClusterId).log\n")
		fOut.write("on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)\n")
		fOut.write("+JobFlavour=\"tomorrow\"\n")
		fOut.write("queue {}".format(totalBinNum))

def produceExecuteScript(binNum: int, binLowerEdge: float, binUpperEdge: float, inputName: str) -> None:
	with open("condor_fit_{}.sh".format(binNum), 'w') as fOut:
		fOut.write("#!/bin/sh\n")
		fOut.write("ulimit -s unlimited\n")
		fOut.write("set -e\n")
		fOut.write("cd /afs/cern.ch/work/z/zhuolinz/MuonTnPTest/CMSSW_10_6_27/src\n")
		fOut.write("export SCRAM_ARCH=slc7_amd64_gcc700\n")
		fOut.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
		fOut.write("eval `scramv1 runtime -sh`\n")
		fOut.write("cd /afs/cern.ch/work/z/zhuolinz/MuonTnPTest/CMSSW_10_6_27/src/MuonAnalysis/TagAndProbe/test/zmumu\n")
		fOut.write("cmsRun fitMuonID_MyAnalysis_MC_arg.py binNum={0} binLower={1} binUpper={2} inputFile={3}_{0}.root".format(binNum, binLowerEdge, binUpperEdge, inputName))
	os.chmod("condor_fit_{}.sh".format(binNum), 0o775)

edgeList = [0, 45, 80, 120, 200, 350, 450, 600]

for index, histEdge in enumerate(edgeList):
	if histEdge != 600:
		binLow = histEdge
		binUp = edgeList[index + 1]
		produceExecuteScript(index, binLow, binUp, args.f)
	else: break

produceCondorScript(len(edgeList) - 1)
