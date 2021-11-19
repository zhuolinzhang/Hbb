import glob
from typing import List
import Tools.CheckCRABResults as CheckResults
import Tools.CopySE2lxslc as CopyFiles
import Tools.haddFiles as Hadd
import Tools.GenerateReduceRDFScript as GenSkim
import argparse
import os
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description="This script can query and copy the result of CRAB jobs if you specify a .json file which recorded all submitted datasets.", epilog="If you use -s to specify a .json file, this script can only find MC samples or DATA once.")
parser.add_argument("-m", "--mode", type=int, help='''1 - Only check results
2 - Check results and copy files 
3 - Mode 2 and generate HTCondor scripts
4 - Mode 3 and generate skim scripts''')
parser.add_argument("--clean", help="Delete all source files", action='store_true')
parser.add_argument("-t", "--task", type=str, help="Input the task name (e.g. ZHTree)")
parser.add_argument("-d", "--date", type=str, help="Input the date (YYMMDD)")
parser.add_argument("-f", type=str, default=None, help="Dataset path list")
parser.add_argument("-haddLocal", action="store_true", help="hadd samples locally w/o generate HTCondor scripts")
parser.add_argument("-q", type=str, default="/publicfs/cms/user/zhangzhuolin/CRABResult", help='''The home path of save query result
The default path is /publicfs/cms/user/zhangzhuolin/CRABResult''')
parser.add_argument("-skim", default="/publicfs/cms/user/zhangzhuolin/TTreeReducer", help='''The path of skimmed TTree
The default path is /publicfs/cms/user/zhangzhuolin/TTreeReducer''')
args = parser.parse_args()

def scanFolderSize(path: str) -> str:
    pathList = glob.glob("{}/*.root".format(path))
    if len(pathList) == 1:
        print("{} only have one .root file, copy it to parent folder!")
        return "tiny"
    elif sum(os.path.getsize("{}".format(f)) * 1e-9 for f in pathList) > 50: # large than 50 GB
        return "huge"
    else: return "normal"

def runT22T3(queryResultPath: str, skimTTreePath: str, taskName: str, taskDate: str, modeNum: int, jsonFileList: List[str]) -> None:
    haddScriptSavePath = "{}/{}_{}/{}".format(queryResultPath, taskName, taskDate, "mergeJobsSubmit")
    haddJobCounter = 0
    hugeFolderList = []
    if modeNum in range(1, 5):
        queryResult = CheckResults.queryCRABResults(queryResultPath, taskName, taskDate, jsonFileList)
        if modeNum in range(2, 5):
            t3Directory = '/publicfs/cms/user/zhangzhuolin/target_files/{}_{}'.format(args.task, args.date)
            for category, campaignDict in queryResult.items():
                for campaign, dataset in campaignDict.items():
                    for datasetName in dataset:
                        jobName = "{}_{}_{}".format(datasetName, taskName, taskDate)
                        CopyFiles.copyFiles(t3Directory, jobName, datasetName, category, campaign)
                        if modeNum in range(3, 5):
                            if args.haddLocal:
                                Hadd.haddFiles(t3Directory, jobName, datasetName, args.clean, campaign)
                            else:
                                mergeSourcePath = "{}/{}_{}".format(t3Directory, datasetName, campaign)
                                mergedPath = "{}/{}_{}.root".format(t3Directory, datasetName, campaign)
                                status = scanFolderSize(mergeSourcePath)
                                if status == "huge":
                                    hugeDict = {}
                                    hugeDict["primaryName"] = datasetName
                                    hugeDict["category"] = category
                                    hugeDict["campaign"] = campaign
                                    hugeFolderList.append(hugeDict)
                                    continue
                                Hadd.generateScripts(haddScriptSavePath, mergeSourcePath, mergedPath, haddJobCounter, campaign)
                                haddJobCounter += 1
    else: raise SystemError("The mode number is wrong! Please execute the script and correct the mode number!")
    if haddJobCounter > 0:
        print("Hadd: hep_sub {}/haddJobSubmit_\"%{{ProcId}}\".sh -n {}".format(haddScriptSavePath, haddJobCounter))
    if modeNum in range(4, 5):
        skimScripSavePath = "{}/{}_{}/{}".format(
            queryResultPath, taskName, taskDate, "ReduceScript.sh")
        skimTargetPath = "{}/{}_{}".format(skimTTreePath, taskName, taskDate)
        skimMacroPath = "{}/ntupleSkimmer.py".format(skimTTreePath)
        GenSkim.generateScriptInOne(
            skimScripSavePath, skimTargetPath, queryResult, skimMacroPath, t3Directory)
        if len(hugeFolderList) > 0:
            for hugeDataset in hugeFolderList:
                skimScriptParentFolder = "{}/{}_{}/{}".format(queryResultPath, taskName, taskDate, "SkimInCondor")
                skimScriptDatasetFolder = "{}/{}".format(skimScriptParentFolder, hugeDataset["primaryName"])
                skimTargetPath = "{}/{}_{}/{}_{}".format(skimTTreePath, taskName, taskDate, hugeDataset["primaryName"], hugeDataset["campaign"])
                skimMacroPath = "{}/ntupleSkimmerForCondor.py".format(skimTTreePath)
                noCutTrees = glob.glob("{}/{}_{}/*.root".format(t3Directory, hugeDataset["primaryName"], hugeDataset["campaign"]))
                CheckResults.checkOutput(skimScriptParentFolder)
                CheckResults.checkOutput(skimScriptDatasetFolder)
                CheckResults.checkOutput(skimTargetPath)
                GenSkim.generateScripts(skimScriptDatasetFolder, skimTargetPath, hugeDataset["primaryName"], hugeDataset["campaign"], skimMacroPath, noCutTrees)

def readDatabasePath(txtPath: str) -> List[str]:
    databasePaths = []
    with open(txtPath, 'r') as f:
        for line in f:
            if line[0] == '#': # if the head of the line is #, ignore the line
                continue
            databasePaths.append(line.rstrip())
    if len(databasePaths) == 0:
        raise SystemExit("The .txt path is invalid, please check it!")
    return databasePaths

# Check VO is activated. But if the VO is invalid, this function doesn't work. I will update to fix this
# bug in the future.
CheckResults.checkVO()
datasetPathList = readDatabasePath(args.f)
runT22T3(args.q, args.skim, args.task, args.date, args.mode, datasetPathList)