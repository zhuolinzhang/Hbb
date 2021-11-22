import json
import argparse
import os
import tarfile
from typing import Dict, List

parse = argparse.ArgumentParser()
parse.add_argument("-i", type=str, help="input .txt file json path list or .json file lists datasets")
parse.add_argument("-o", type=str, default="./output", help="output path, default = ./output")
parse.add_argument("-n", type=str, help="task name e.g. ZHTree, if %%year in task name, will fill the year of dataset automatically")
parse.add_argument("-d", "--date", type=str, help="date (YYMMDD)")
parse.add_argument("-pset", help="The path of config.JobType.psetName (cfg.py) e.g. ZHAnalysis_cfg.py")
parse.add_argument("-psetList", action="extend", nargs="+", type=str, help="The list of config.JobType.psetName (cfg.py) e.g. ZHAnalysis_cfg.py, [UL, ReReco, data]")
parse.add_argument("--temp", type=str, default="crabSkeleton.py", help="the template of carbConfig, default = crabSkeleton.py")
parse.add_argument("-tar", action="store_true", help="Compress all output files as .tar.gz")
parse.add_argument("-pyCfg", default=None, help="The config.JobType.pyCfgParams for datasets")
args = parse.parse_args()

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

def modifySkeleton(skelekonPath: str, taskDate: str) -> List[str]:
    newSkeleton = []
    with open(skelekonPath, 'r') as cfgTemp:
        fileLines = cfgTemp.readlines()
    for line in fileLines:
        if "version = ''" in line:
            line = "version = '{}'\n".format(taskDate)
        newSkeleton.append(line)
    return newSkeleton

def readCfgArgs(argsFile: str, **kwargs) -> List[str]:
    argsDict = {}
    with open(argsFile, 'r') as f:
        argsDict = json.load(f)
    if argsDict["type"] == "campaign":
        return argsDict[kwargs["campaign"]]
    elif argsDict["type"] == "dbs":
        return argsDict[kwargs["datasetFullName"]]
    elif argsDict["type"] == "dataset":
        return argsDict[kwargs["primaryName"]]
    elif argsDict["type"] == "category":
        return argsDict[kwargs["category"]]
    elif argsDict["type"] == "categoryAndCampaign":
        return argsDict[kwargs["category"][kwargs["campaign"]]]
    else: raise SystemError("Your input args json file is wrong! The type name in json file is necessary!")

def generateDatasetCrabLines(taskName: str, datasetPrimaryName: str, datasetDBS: str, psetPath: str, **kwargs) -> List[str]:
    if "%year" in taskName:
        year = kwargs["campaign"].rstrip("ReReco").rstrip("UL")
        taskName = taskName.replace("%year", year)
    requestName = "    config.General.requestName = '{}_{}_' + version\n".format(datasetPrimaryName, taskName)
    inputDataset = "    config.Data.inputDataset = '{}'\n".format(datasetDBS)
    outputTag = "    config.Data.outputDatasetTag = config.General.requestName\n"
    pset = "    config.JobType.psetName = '{}'\n".format(psetPath)
    if kwargs["args"] != None:
        if kwargs["isData"]: argsCategory = "data"
        else: argsCategory = "mc"
        args = "    config.JobType.pyCfgParams={}\n".format(readCfgArgs(kwargs["args"], campaign=kwargs["campaign"], datasetFullName=datasetDBS, primaryName=datasetPrimaryName, category=argsCategory))
    submit = "    crabCommand('submit', config = config)\n"
    emptyLine = "\n"
    datasetList = [requestName, inputDataset, outputTag, pset, submit, emptyLine]
    if kwargs["args"] != None:
        datasetList = [requestName, inputDataset, outputTag, pset, args, submit, emptyLine]
    if kwargs["isData"]:
        lumi = "    config.Data.lumiMask = '{}'\n".format(kwargs["lumiMask"])
        datasetList = [requestName, inputDataset, outputTag, pset, lumi, submit, emptyLine]
        if kwargs["args"] != None:
            datasetList = [requestName, inputDataset, outputTag, pset, args, lumi, submit, emptyLine]
    return datasetList

# if output path is not existed, create the path
if os.path.exists(args.o): pass
else: 
    print("Create the output path {}".format(args.o))
    os.mkdir(args.o)

datasetNameDict = {}
newCrabCfgList = []
newStr = ''
lumiMaskDict = {"2018UL": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt", 
                "2017UL": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                "2016APVUL": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                "2016UL": "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"}

sampleList = readJsonList(args.i)
skeletonList = modifySkeleton(args.temp, args.date)
for dataset in sampleList:
    pset = args.pset
    if args.psetList != None:
        if 'data' == dataset["category"]: 
            pset = args.psetList[2]
        elif 'UL' in dataset["campaign"]: 
            pset = args.psetList[0]
        elif 'ReReco' in dataset["campaign"]: 
            pset = args.psetList[1]
        
    if dataset["category"] == "data":
        datasetBlock = generateDatasetCrabLines(args.n, dataset["primaryName"], dataset["dasName"], pset, isData=True, lumiMask=lumiMaskDict[dataset["campaign"]], campaign=dataset["campaign"], args=args.pyCfg)
    else: 
        datasetBlock = generateDatasetCrabLines(args.n, dataset["primaryName"], dataset["dasName"], pset, isData=False, campaign=dataset["campaign"], args=args.pyCfg)

    skeletonList += datasetBlock

crabFileName = "crabConfig_{}_{}.py".format(args.n.rstrip("%year"), args.date)
print("Generate {}".format(crabFileName))
with open(args.o + '/' + crabFileName, 'w') as crabCfg:
    crabCfg.writelines(skeletonList)

if args.tar:
    tarFiles(args.n, args.date, args.o)