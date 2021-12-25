import os
import argparse
import json
import glob
from typing import List, Dict

def generateScriptInOne(scriptSavePath: str, skimTTreeSaveFolder: str, queryList: Dict[str, Dict[str, List[str]]], macroPath: str, originTTreeFolder: str) -> None:
    with open(scriptSavePath, 'w') as f:
        f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n')
        f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
        f.write('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh\n')
        for campaignDict in queryList.values():
            for campaign, datasetList in campaignDict.items():
                for dataset in datasetList:
                    originTTreePath = "{}/{}_{}.root".format(originTTreeFolder, dataset, campaign)
                    skimTTreeSavePath = "{}/{}_{}.root".format(skimTTreeSaveFolder, dataset, campaign)
                    f.write('python3 {} -i {} -o {} -c {}\n'.format(macroPath, originTTreePath, skimTTreeSavePath, campaign))
    os.chmod(scriptSavePath, 0o755)
    print("Skim Command: sh {}".format(scriptSavePath))

def readJson(jsonFile: str) -> list:
    with open(jsonFile) as f:
        return json.load(f)

def generateScripts(skimScriptSaveFolder: str, skimTTreeSaveFolder: str, dataset: str, campaign: str, macroPath: str, originTTreeFolder: list) -> None:
    for rootFile in originTTreeFolder:
        scriptSavePath = "{}/reduce_{}.sh".format(skimScriptSaveFolder, originTTreeFolder.index(rootFile))
        with open(scriptSavePath, 'w') as f:
            f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n')
            f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
            f.write('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh\n')
            skimTTreeSavePath = "{}/{}_{}/{}".format(skimTTreeSaveFolder, dataset, campaign, rootFile.split('/')[-1])
            f.write('python3 {} -i {} -o {} -c {}\n'.format(macroPath, rootFile, skimTTreeSavePath, campaign))
        os.chmod(scriptSavePath, 0o755)
        print("Script {} is generated!".format(scriptSavePath))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="/publicfs/cms/user/zhangzhuolin/CRABResult", help="The default path of CRAB result")
    parser.add_argument("-t", "--task", type=str, help="The task name of CRAB job. e.g. ZHTree")
    parser.add_argument("-d", "--date", type=str, help="The task date of CRAB job. e.g. 210412")
    parser.add_argument("-f", help="The .json file to generate the script")
    args = parser.parse_args()
    t3OriginPath = '/publicfs/cms/user/zhangzhuolin/target_files'
    t3SkimPath = '/publicfs/cms/user/zhangzhuolin/TTreeReducer'
    macroName = '/ntupleSkimmer.py'
    macroPath = t3SkimPath + macroName
    taskFilePath = t3OriginPath + '/' + args.task + "_" + args.date
    skimFolderPath = t3SkimPath + '/' + args.task + "_" + args.date
    checkResultPath = args.path + "/" + args.task + "_" + args.date
    resultListPath = checkResultPath + "/" + "QueryResult.json"
    if args.f != None:
        resultListPath = args.f
    resultList = readJson(resultListPath)
    skimScriptSavePath = checkResultPath + "/" + "ReduceScript.sh"
    generateScriptInOne(skimScriptSavePath, skimFolderPath, resultList, macroPath, taskFilePath)
    if len(resultList) > 0:
        print("*" * 60)
        print("The skimming script path: {}".format(skimScriptSavePath))