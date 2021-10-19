import os
import argparse
import json
from typing import List, Dict

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, default="/publicfs/cms/user/zhangzhuolin/CRABResult", help="The default path of CRAB result")
parser.add_argument("-t", "--task", type=str, help="The task name of CRAB job. e.g. ZHTree")
parser.add_argument("-d", "--date", type=str, help="The task date of CRAB job. e.g. 210412")
args = parser.parse_args()

def generateScript(scriptSavePath: str, skimTTreeSaveFolder: str, originTTrees: Dict[List[str]], macroPath: str, originTTreeFolder: str) -> None:
    with open(scriptSavePath, 'w') as f:
        f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n')
        f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
        f.write('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh\n')
        for campaign, datasetList in originTTrees.items():
            for dataset in datasetList:
                originTTreePath = "{}/{}_{}.root".format(originTTreeFolder, dataset, campaign)
                skimTTreeSavePath = "{}/{}_{}.root".format(skimTTreeSaveFolder, dataset, campaign)
                f.write('python3 {} -i {} -o {} -c {}\n'.format(macroPath, originTTreePath, skimTTreeSavePath, campaign))
    os.chmod(scriptSavePath, 0o755)
    print("Script {} is generated!".format(scriptSavePath))

def readJson(jsonFile: str) -> list:
    with open(jsonFile) as f:
        return json.load(f)

t3OriginPath = '/publicfs/cms/user/zhangzhuolin/target_files'
t3SkimPath = '/publicfs/cms/user/zhangzhuolin/TTreeReducer'
macroName = '/ntupleSkimmer.py'
macroPath = t3SkimPath + macroName
taskFilePath = t3OriginPath + '/' + args.task + "_" + args.date
skimFolderPath = t3SkimPath + '/' + args.task + "_" + args.date
checkResultPath = args.path + "/" + args.task + "_" + args.date
mcListPath = checkResultPath + "/" + "MCList.json"
dataListPath = checkResultPath + "/" + "DataList.json"

mcList = readJson(mcListPath)
dataList = readJson(dataListPath)

mcScriptSavePath = checkResultPath + "/" + "MCReduceScript.sh"
dataScriptSavePath = checkResultPath + "/" + "DataReduceScript.sh"
generateScript(mcScriptSavePath, skimFolderPath, mcList, macroPath, taskFilePath)
generateScript(dataScriptSavePath, skimFolderPath, dataList, macroPath, taskFilePath)

if len(mcList) > 0:
    print("*" * 60)
    print("The MC skimming script path: {}".format(mcScriptSavePath))
if len(dataList) > 0:
    print("*" * 60)
    print("The DATA skimming script path: {}".format(dataScriptSavePath))