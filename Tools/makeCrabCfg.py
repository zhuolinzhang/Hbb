import json
import argparse
import os
import tarfile

parse = argparse.ArgumentParser()
parse.add_argument("-i", type=str, help="input json file")
parse.add_argument("-o", type=str, default="./output", help="output path, default = ./output")
parse.add_argument("-n", type=str, help="task name e.g. ZHTree")
parse.add_argument("-d", "--date", type=str, help="date (YYMMDD)")
parse.add_argument("--pset", action="extend", nargs="+", type=str, help="The list of config.JobType.psetName, cfg.py e.g. ZHAnalysis_cfg.py, [UL, ReReco, data]")
parse.add_argument("--temp", type=str, default="crabConfig.py", help="the template of carbConfig, default = crabConfig.py")
parse.add_argument("-tar", action="store_true", help="Compress all output files as .tar.gz")
args = parse.parse_args()

def tarFiles(taskName: str, taskDate: str, outputPath: str) -> None:
    fileList = os.listdir(outputPath)
    tarball = tarfile.open("./{}_{}.tgz".format(taskName, taskDate), "w|gz")
    for file in fileList:
        tarball.add(outputPath + '/' + file)
    print("The output tarball {}_{} is created!".format(taskName, taskDate))

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

with open(args.temp, 'r') as cfgTemp:
    fileLines = cfgTemp.readlines()

with open(args.i, 'r') as datasetInfo:
    sampleList = json.load(datasetInfo)

for dataset in sampleList:
    if 'UL' in dataset["campaign"]: pset = args.pset[0]
    elif 'ReReco' in dataset["campaign"]: pset = args.pset[1]
    if 'data' in dataset["category"]: pset = args.pset[2]
    for i in fileLines:
        newStr = i
        if 'config.JobType.psetName' in i:
            newStr = "config.JobType.psetName = '{}'\n".format(pset)
        if "config.General.requestName" in i:
            newStr = "config.General.requestName = '{}_{}_{}'\n".format(dataset["primaryName"], args.n, args.date)
        if "config.Data.inputDataset" in i:
            newStr = "config.Data.inputDataset = '{}'\n".format(dataset["dasName"])
        if "config.Data.outputDatasetTag" in i:
            if 'data' in dataset["category"]:
                newStr = "config.Data.outputDatasetTag = '{}_{}_{}'\nconfig.Data.lumiMask = '{}'\n".format(dataset["primaryName"], args.n, args.date, lumiMaskDict[dataset["campaign"]])
            else:
                newStr = "config.Data.outputDatasetTag = '{}_{}_{}'\n".format(dataset["primaryName"], args.n, args.date)
        newCrabCfgList.append(newStr)
    crabFileName = "crabConfig_{}_{}.py".format(dataset["primaryName"], dataset["campaign"])
    print("Generate {}".format(crabFileName))
    with open(args.o + '/' + crabFileName, 'w') as crabCfg:
        crabCfg.writelines(newCrabCfgList)
    newCrabCfgList = []

if args.tar:
    tarFiles(args.n, args.date, args.o)