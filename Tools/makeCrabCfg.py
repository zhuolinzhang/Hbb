import json
import argparse
import os
import tarfile
import copy
from typing import Dict, List, Tuple

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="input .txt file json path list or .json file lists datasets")
parser.add_argument("inputConfig", type=str, help="input json path recording the configuration of the CRAB cfg")
parser.add_argument("-o", type=str, default="./output", help="output path, default = ./output")
parser.add_argument("--temp", type=str, default="crabSkeleton.py", help="the template of carbConfig, default = crabSkeleton.py")
parser.add_argument("-tar", action="store_true", help="Compress all output files as .tar.gz")
args = parser.parse_args()

def tarFiles(taskName: str, taskDate: str, outputPath: str) -> None:
    fileList = os.listdir(outputPath)
    tarball = tarfile.open("./{}_{}.tgz".format(taskName, taskDate), "w|gz")
    for file in fileList:
        tarball.add(outputPath + '/' + file)
    print("The output tarball {}_{} is created!".format(taskName, taskDate))

def readJsonList(path: str) -> List[Dict[str, str]]:
    jsonPathList = []
    if path.endswith(".txt"):
        with open(path, 'r') as f:
            for line in f:
                if line[0] == '#': continue
                with open(line.rstrip(), 'r') as fJson:
                    jsonPathList += json.load(fJson)
    elif path.endswith(".json"):
        with open(path, 'r') as f:
            jsonPathList = json.load(f)
    return jsonPathList

def modifySkeleton(skeletonPath: str, taskDate: str) -> List[str]:
    '''
        Add date infomation to the skeleton
    '''
    newSkeleton = []
    with open(skeletonPath, 'r') as cfgTemp:
        fileLines = cfgTemp.readlines()
    for line in fileLines:
        if "version = ''" in line:
            line = "version = '{}'\n".format(taskDate)
        newSkeleton.append(line)
    return newSkeleton

def generateDatasetCrabLines(taskName: str, datasetPrimaryName: str, datasetDBS: str, psetPath: str, **kwargs) -> List[str]:
    if "%year" in taskName:
        year = kwargs["campaign"].rstrip("ReReco").rstrip("UL")
        taskName = taskName.replace("%year", year)
    requestName = "    config.General.requestName = '{}_{}_' + version\n".format(datasetPrimaryName, taskName)
    inputDataset = "    config.Data.inputDataset = '{}'\n".format(datasetDBS)
    outputTag = "    config.Data.outputDatasetTag = config.General.requestName\n"
    pset = "    config.JobType.psetName = '{}'\n".format(psetPath)
    if "args" in kwargs:
        args = "    config.JobType.pyCfgParams={}\n".format(kwargs["args"])
    submit = "    crabCommand('submit', config = config)\n"
    emptyLine = "\n"
    datasetList = [requestName, inputDataset, outputTag, pset, submit, emptyLine]
    if "args" in kwargs:
        datasetList = [requestName, inputDataset, outputTag, pset, args, submit, emptyLine]
    if "lumiMask" in kwargs:
        lumi = "    config.Data.lumiMask = '{}'\n".format(kwargs["lumiMask"])
        datasetList = [requestName, inputDataset, outputTag, pset, lumi, submit, emptyLine]
        if kwargs["args"] != None:
            datasetList = [requestName, inputDataset, outputTag, pset, args, lumi, submit, emptyLine]
    return datasetList

def readNameAndDate(crabCfg: dict) -> Tuple[str, str]:
    return crabCfg["name"], crabCfg["date"]

def produceCrabBlockByCategoryAndCampaign(crabCfg: dict, datasetList: list) -> None:
    taskName, taskDate = readNameAndDate(crabCfg)
    skeletonList = modifySkeleton(args.temp, taskDate)
    skeletonLen = len(skeletonList)
    skeletonDict = {}
    for category, campaignPsetCfg in crabCfg["config"].items():
        if category == "type": continue
        if category == "data":
            for campaign, psetCfgPair in campaignPsetCfg.items():
                skeletonDict["{}_{}".format(category, campaign)] = copy.deepcopy(skeletonList)
                for dataset in datasetList:
                    if dataset["category"] == "data" and dataset["campaign"] == campaign:
                        if crabCfg["config"]["type"] == "psetCfg":
                            datasetBlock = generateDatasetCrabLines(taskName, dataset["primaryName"], dataset["dasName"], psetCfgPair["pset"], lumiMask=lumiMaskDict[dataset["campaign"]], campaign=dataset["campaign"], args=psetCfgPair["pyCfg"])
                        elif crabCfg["config"]["type"] == "pset":
                            datasetBlock = generateDatasetCrabLines(taskName, dataset["primaryName"], dataset["dasName"], psetCfgPair["pset"], lumiMask=lumiMaskDict[dataset["campaign"]], campaign=dataset["campaign"])
                        else: raise SystemError("The type in config is wrong!")
                        skeletonDict["{}_{}".format(category, campaign)] += datasetBlock
        if category == "mc":
            for campaign, psetCfgPair in campaignPsetCfg.items():
                skeletonDict["{}_{}".format(category, campaign)] = copy.deepcopy(skeletonList)
                for dataset in datasetList:
                    if dataset["category"] != "data" and dataset["campaign"] == campaign:
                        if crabCfg["config"]["type"] == "psetCfg":
                            datasetBlock = generateDatasetCrabLines(taskName, dataset["primaryName"], dataset["dasName"], psetCfgPair["pset"], campaign=dataset["campaign"], args=psetCfgPair["pyCfg"])
                        elif crabCfg["config"]["type"] == "pset":
                            datasetBlock = generateDatasetCrabLines(taskName, dataset["primaryName"], dataset["dasName"], psetCfgPair["pset"], campaign=dataset["campaign"])
                        else: raise SystemError("The type in config is wrong!")
                        skeletonDict["{}_{}".format(category, campaign)] += datasetBlock
    for categoryAndCampaign, crabBlocks in skeletonDict.items():
        if (len(skeletonDict[categoryAndCampaign]) > skeletonLen): # Avoid generate empty CRAB scripts
            print("Generate CRAB script in {}".format(categoryAndCampaign))
            writeCrabCfg(args.o, crabBlocks, taskName, taskDate, categoryCampaign=categoryAndCampaign)

def readCrabCfgJson(path: str, databaseList: list) -> None:
    cfgDict = {}
    with open(path, 'r') as f:
        cfgDict = json.load(f)
    if cfgDict["type"] == "categoryAndCampaign":
        produceCrabBlockByCategoryAndCampaign(cfgDict, databaseList)
    if args.tar:
       tarFiles(cfgDict["name"], cfgDict["date"], args.o) 

def writeCrabCfg(outputFolder: str, crabItems: List[str], name: str, date: str, **kwargs) -> None:
    fileName = "crabConfig_{}_{}.py".format(name.rstrip("%year"), date)
    if "categoryCampaign" in kwargs:
        fileName = "crabConfig_{}_{}_{}.py".format(name.rstrip("%year"), date, kwargs["categoryCampaign"])
    with open("{}/{}".format(outputFolder, fileName), 'w') as fOut:
        fOut.writelines(crabItems)

# if output path is not existed, create the path
if os.path.exists(args.o): pass
else: 
    print("Create the output path {}".format(args.o))
    os.mkdir(args.o)

lumiMaskDict = {"2018UL": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt", 
                "2017UL": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                "2016APVUL": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                "2016UL": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"}

sampleList = readJsonList(args.input)
readCrabCfgJson(args.inputConfig, sampleList)