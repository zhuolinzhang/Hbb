import json
import argparse
import os
import tarfile
from typing import Dict, List

parse = argparse.ArgumentParser()
parse.add_argument("-i", type=str, help="input .txt file json path list")
parse.add_argument("-o", type=str, default="./output", help="output path, default = ./output")
parse.add_argument("-n", type=str, help="task name e.g. ZHTree, if %year in task name, will fill the year of dataset automatically")
parse.add_argument("-d", "--date", type=str, help="date (YYMMDD)")
parse.add_argument("-pset", action="extend", nargs="+", type=str, help="The list of config.JobType.psetName, cfg.py e.g. ZHAnalysis_cfg.py, [UL, ReReco, data]")
parse.add_argument("--temp", type=str, default="crabSkeleton.py", help="the template of carbConfig, default = crabSkeleton.py")
parse.add_argument("-tar", action="store_true", help="Compress all output files as .tar.gz")
args = parse.parse_args()

def tarFiles(taskName: str, taskDate: str, outputPath: str) -> None:
    fileList = os.listdir(outputPath)
    tarball = tarfile.open("./{}_{}.tgz".format(taskName, taskDate), "w|gz")
    for file in fileList:
        tarball.add(outputPath + '/' + file)
    print("The output tarball {}_{} is created!".format(taskName, taskDate))

def readJsonList(path: str) -> List[Dict[str, str]]:
    jsonPathList = []
    with open(path, 'r') as f:
        for line in f:
            if line[0] == '#': continue
            with open(line.rstrip(), 'r') as fJson:
                jsonPathList += json.load(fJson)
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

def generateDatasetCrabLines(taskName: str, datasetPrimaryName: str, datasetDBS: str, dataFlag: bool, psetPath: str, **kwargs) -> List[str]:
    if "%year" in taskName:
        year = kwargs["campaign"].rstrip("ReReco").rstrip("UL")
        taskName = taskName.replace("%year", year)
    requestName = "    config.General.requestName = '{}_{}_' + version\n".format(datasetPrimaryName, taskName)
    inputDataset = "    config.Data.inputDataset = '{}'\n".format(datasetDBS)
    outputTag = "    config.Data.outputDatasetTag = config.General.requestName\n"
    pset = "    config.JobType.psetName = '{}'\n".format(psetPath)
    submit = "    crabCommand('submit', config = config)\n"
    emptyLine = "\n"
    datasetList = [requestName, inputDataset, outputTag, pset, submit, emptyLine]
    if dataFlag:
        lumi = "    config.Data.lumiMask = '{}'\n".format(kwargs["lumiMask"])
        datasetList = [requestName, inputDataset, outputTag, pset, lumi, submit, emptyLine]
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
    if 'data' == dataset["category"]: 
        pset = args.pset[2]
        isData = True
    elif 'UL' in dataset["campaign"]: 
        pset = args.pset[0]
        isData = False
    elif 'ReReco' in dataset["campaign"]: 
        pset = args.pset[1]
        isData = False
    
    if isData:
        datasetBlock = generateDatasetCrabLines(args.n, dataset["primaryName"], dataset["dasName"], isData, pset, lumiMask=lumiMaskDict[dataset["campaign"]], campaign=dataset["campaign"])
    else: 
        datasetBlock = generateDatasetCrabLines(args.n, dataset["primaryName"], dataset["dasName"], isData, pset, campaign=dataset["campaign"])

    skeletonList += datasetBlock

crabFileName = "crabConfig_{}_{}.py".format(args.n.rstrip("%year"), args.date)
print("Generate {}".format(crabFileName))
with open(args.o + '/' + crabFileName, 'w') as crabCfg:
    crabCfg.writelines(skeletonList)

if args.tar:
    tarFiles(args.n, args.date, args.o)