# Place this file to TnP Trees folder. It will produce skim scripts for HTCondor in ./scripts

import glob
import os

def checkOutput(path: str) -> None:
	if os.path.exists(path): pass
	else: os.mkdir(path)

pwdFolder = os.getcwd()
outputScriptFolder = "{}/scripts".format(pwdFolder)
outputTnPTreeFolder = "{}/trees".format(pwdFolder)
checkOutput(outputScriptFolder)
checkOutput(outputTnPTreeFolder)

tnpTreeList = glob.glob("{}/*.root".format(pwdFolder))
for file in tnpTreeList:
	indexNum = tnpTreeList.index(file)
	with open("{}/skim_{}.sh".format(outputScriptFolder, indexNum), 'w') as f:
		f.write("#!/bin/bash\n")
		f.write("source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.02/x86_64-centos7-gcc48-opt/bin/thisroot.sh\n")
		f.write("/cms/user/zhangzhuolin/TTreeReducer/TnPUtils/skimTree {} {}/skim_{}.root -r \"*\" -k \"mass pt abseta Loose PFIsoTight\"\n".format(file, outputTnPTreeFolder, indexNum))
	os.chmod("{}/skim_{}.sh".format(outputScriptFolder, indexNum), 0o775)
	if indexNum % 100 == 0:
		print("Produce Script {}...".format(indexNum + 1))
print("HTCondor: hep_sub {}/skim_\"%{{ProcId}}\".sh -n {}".format(outputScriptFolder, len(tnpTreeList)))
