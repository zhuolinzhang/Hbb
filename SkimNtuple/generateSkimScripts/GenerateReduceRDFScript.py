import os
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, default="/publicfs/cms/user/zhangzhuolin/CRABResult", help="The default path of CRAB result")
parser.add_argument("-t", "--task", type=str, help="The task name of CRAB job. e.g. ZHTree")
parser.add_argument("-d", "--date", type=str, help="The task date of CRAB job. e.g. 210412")
parser.add_argument("-j", help="The .json file of MC samples")
args = parser.parse_args()

def readLocalList(listFilePath):
    fileList = []
    with open(listFilePath, 'r') as f:
        fileListOrigin = f.readlines()
        for i in fileListOrigin:
            fileList.append(i.rstrip())
    return fileList

def generateScripts(scriptSavePath, skimTTreeSavePath, originTTreePath, macroPath, scriptNum, datasetCampaign):
    if os.path.exists(scriptSavePath): pass
    else: os.mkdir(scriptSavePath)
    fileName = 'SkimJobSubmit_' + str(scriptNum) + '.sh'
    with open(scriptSavePath + '/' + fileName, 'w') as f:
        f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n')
        f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
        f.write('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh\n')
        f.write('python3 {} -i {} -o {} -c {}'.format(macroPath, originTTreePath, skimTTreeSavePath, datasetCampaign))
    os.chmod(scriptSavePath +"/" + fileName, 0o755)
    print("Script {} is generated!".format(fileName))

def readJson(jsonFile: str) -> list:
    with open(jsonFile) as f:
        return json.load(f)

def returnMCCampaign(mcList: list, jsonList: list) -> dict:
    campaignDict = {}
    for sample in mcList:
        fullName = ''
        for mcDict in jsonList:
            for names in mcDict.values():
                if sample == names:
                    fullName = mcDict['dasName']
                    break
        if 'Summer20UL' in fullName or 'Summer19UL' in fullName:
            camp = 'UL'
        else: camp = 'ReReco'
        if 'upgrade2018' in fullName: years = '2018'
        elif 'mc2017' in fullName: years = '2017'
        elif 'mcRun2' in fullName: 
            years = '2016'
            if 'preVFP' in fullName: years = '2016APV'
        campaign = years + camp
        campaignDict[sample] = campaign
    return campaignDict

def returnDataCampaign(dataList: list) -> dict:
    campaignDict = {}
    for data in dataList:
        if '2018' in data: campaignDict[data] = '2018UL'
        elif '2017' in data: campaignDict[data] = '2017UL' 
    return campaignDict

t3OriginPath = '/publicfs/cms/user/zhangzhuolin/target_files'
t3SkimPath = '/publicfs/cms/user/zhangzhuolin/TTreeReducer'
macroName = '/ntupleSkimmer.py'
macroPath = t3SkimPath + macroName
taskFilePath = t3OriginPath + '/' + args.task + "_" + args.date
skimFolderPath = t3SkimPath + '/' + args.task + "_" + args.date
checkResultPath = args.path + "/" + args.task + "_" + args.date
mcListPath = checkResultPath + "/" + "MCList.txt"
dataListPath = checkResultPath + "/" + "DataList.txt"

mcList = readLocalList(mcListPath)
dataList = readLocalList(dataListPath)

dataCampaign = returnDataCampaign(dataList)
if args.j != None: 
    mcJsonInfo = readJson(args.j)
    mcCampagin = returnMCCampaign(mcList, mcJsonInfo)

mcScriptSavePath = checkResultPath + "/" + "MCReduceScripts"
dataScriptSavePath = checkResultPath + "/" + "DataReduceScripts"
for i in mcList:
    print("Generate the script of {}.".format(i))
    mcSourcePath = taskFilePath + '/' + i + '.root'
    skimFilePath = skimFolderPath + '/' + i + '.root'
    generateScripts(mcScriptSavePath, skimFilePath, mcSourcePath, macroPath, mcList.index(i), mcCampagin[i])

for i in dataList:
    print("Generate the script of {}.".format(i))
    dataSourcePath = taskFilePath + '/' + i + '.root'
    skimFilePath = skimFolderPath + '/' + i + '.root'
    generateScripts(dataScriptSavePath, skimFilePath, dataSourcePath, macroPath, dataList.index(i), dataCampaign[i])

if len(mcList) > 0:
    print("*" * 60)
    print("The MC skimming script path: {}".format(mcScriptSavePath))
if len(dataList) > 0:
    print("*" * 60)
    print("The DATA skimming script path: {}".format(dataScriptSavePath))
    