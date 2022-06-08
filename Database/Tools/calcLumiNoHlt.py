import json
import os
from typing import List

def readLumi(resultList: List[str]) -> float:
    findLine = False
    lumiRead = 0
    for line in reversed(resultList):
        if "#Check JSON" in line:
            findLine = True
            continue
        if findLine:
            lumiRead = float(line.split(',')[-1].rstrip())
            break
    return lumiRead

lumiMaskDict = {"2018": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt", 
                "2017": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                "2016": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                "2016APV": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"}
#hltDict = {"2018": "HLT_IsoMu20_v*", "2017": "HLT_IsoMu20_v*", "2016": "HLT_Mu17_Mu8_v*", "2016APV": "HLT_Mu17_v*"} # pre-scale trigger
hltDict = {"2018": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*", "2017": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*", "2016": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*", "2016APV": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*"} # physics trigger
totalLumiPerYear = {"2016APV": 0, "2016": 0, "2017": 0, "2018": 0}
runInfo = {}
preVfpRunNum = [277932, 277934, 277981, 277991, 277992, 278017, 278018, 278167, 278175, 278193, 278239, 278240, 278273, 278274, 278288, 278289, 278290, 278308, 278309, 278310, 278315, 278345, 278346, 278349, 278366, 278406, 278509, 278761, 278770, 278806, 278807]
postVfpRunNum = [278769, 278801, 278802, 278803, 278804, 278805, 278808]
with open("./runNum.json", 'r') as f:
    runInfo = json.load(f)

lumiResult = []

for year, datasetsInfo in runInfo.items():
    for name, runNums in datasetsInfo.items():
        #print('brilcalc lumi -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i {} --begin {} --end {}'.format(lumiMaskDict[year], runNums[0], runNums[1]))
        if name != "DoubleMuon2016F":
            fBrilCalc = os.popen('brilcalc lumi -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i {} --begin {} --end {} --output-style csv'.format(lumiMaskDict[year], runNums[0], runNums[1]))
            result = fBrilCalc.readlines()
            lumi = readLumi(result)
        else:
            lumi = 0
            if year == "2016APV":
                runList2016F = preVfpRunNum
            else: runList2016F = postVfpRunNum
            for runNum2016F in runList2016F:
                fBrilCalc = os.popen('brilcalc lumi -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i {} -r {} --output-style csv'.format(lumiMaskDict[year], runNum2016F))
                resultSingleRun = fBrilCalc.readlines()
                singleRunLumi = readLumi(resultSingleRun)
                lumi += singleRunLumi
        print("{} lumi: {}".format(name, lumi))
        lumiResult.append("{} lumi: {}\n".format(name, lumi))
        totalLumiPerYear[year] += lumi

for year, totalLumi in totalLumiPerYear.items():
    print("{} Total Lumi: {}".format(year, totalLumi))
    lumiResult.append("{} Total Lumi: {}\n".format(year, totalLumi))
with open("./calcMultiResultNoHlt.txt", 'w') as f:
    f.writelines(lumiResult)
