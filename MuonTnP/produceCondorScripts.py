import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="The name of input root file name w/o index number")
args = parser.parse_args()

def produceCondorScript(etaBinNum: int, totalPtBinNum: int) -> None:
	with open("condor_fit_{}.sub".format(etaBinNum), 'w') as fOut:
		fOut.write("executable = condor_fit_{}_$(ProcId).sh\n".format(etaBinNum))
		fOut.write("output                = $(ClusterId).$(ProcId).out\n")
		fOut.write("error                 = $(ClusterId).$(ProcId).err\n")
		fOut.write("log                   = $(ClusterId).log\n")
		fOut.write("on_exit_hold = (ExitBySignal == True) || (ExitCode != 0)\n")
		fOut.write("+JobFlavour=\"tomorrow\"\n")
		fOut.write("queue {}".format(totalPtBinNum))

def produceExecuteScript(ptBinNum: int, etaBinNum: int, inputName: str, **kwargs) -> None:
	with open("condor_fit_{}_{}.sh".format(etaBinNum, ptBinNum), 'w') as fOut:
		fOut.write("#!/bin/sh\n")
		fOut.write("ulimit -s unlimited\n")
		fOut.write("set -e\n")
		fOut.write("cd /afs/cern.ch/work/z/zhuolinz/MuonTnPTest/CMSSW_10_6_27/src\n")
		fOut.write("export SCRAM_ARCH=slc7_amd64_gcc700\n")
		fOut.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
		fOut.write("eval `scramv1 runtime -sh`\n")
		fOut.write("cd /afs/cern.ch/work/z/zhuolinz/MuonTnPTest/CMSSW_10_6_27/src/MuonAnalysis/TagAndProbe/test/zmumu\n")
		fOut.write("cmsRun fitMuonID_MyAnalysis_MC_arg.py ptBinNum={0} ptBinLower={1} ptBinUpper={2} etaBinNum={3} etaBinLower={4} etaBinUpper={5} inputFile={6}_{3}_{0}.root".format(ptBinNum, kwargs["ptBinLower"], kwargs["ptBinUpper"], etaBinNum, kwargs["etaBinLower"], kwargs["etaBinUpper"], inputName))
	os.chmod("condor_fit_{}_{}.sh".format(etaBinNum, ptBinNum), 0o775)

ptEdgeList = [15, 20, 25, 30, 40, 50, 60, 120]
absEtaEdgeList = [0, 0.9, 1.2, 2.1, 2.4]

for etaIndex, etaHistEdge in enumerate(absEtaEdgeList):
	if etaHistEdge != 2.4:
		etaBinLow = etaHistEdge
		etaBinUp = absEtaEdgeList[etaIndex + 1]
	else: break
	for ptIndex, ptHistEdge in enumerate(ptEdgeList):
		if ptHistEdge != 120:
			ptBinLow = ptHistEdge
			ptBinUp = ptEdgeList[ptIndex + 1]
			produceExecuteScript(ptIndex, etaIndex, args.f, ptBinLower=ptBinLow, ptBinUpper=ptBinUp, etaBinLower=etaBinLow, etaBinUpper=etaBinUp)
		else: break
	produceCondorScript(etaIndex, len(ptHistEdge) - 1)