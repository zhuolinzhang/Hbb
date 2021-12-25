import json
import os

lumiMaskDict = {"2018": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt", 
                "2017": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                "2016": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                "2016APV": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"}
hltDict = {"2018": "HLT_IsoMu20_v*", "2017": "HLT_IsoMu20_v*", "2016": "HLT_Mu17_Mu8_v*", "2016APV": "HLT_Mu17_v*"}
runInfo = {}
with open("./runNum.json", 'r') as f:
	runInfo = json.load(f)

lumiResult = []

for year, datasetsInfo in runInfo.items():
	for name, runNums in datasetsInfo.items():
		fBrilCalc = os.popen('brilcalc lumi -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i {} --begin {} --end {} --hltpath {}'.format(lumiMaskDict[year], runNums[0], runNums[1], hltDict[year]))
		result = fBrilCalc.readlines()
		for line in reversed(result):
			if "#Sum recorded" in line:
				print("{} lumi: {}".format(name, line.rstrip()))
				lumiResult.append("{} lumi: {}\n".format(name, line.rstrip()))
				break

with open("./calcMultiResult.txt", 'w') as f:
	f.writelines(lumiResult)