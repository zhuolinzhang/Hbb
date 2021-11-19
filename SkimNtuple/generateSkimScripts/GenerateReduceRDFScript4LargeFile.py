import os
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, default="/publicfs/cms/user/zhangzhuolin/CRABResult", help="The default path of CRAB result")
parser.add_argument("-t", "--task", type=str, help="The task name of CRAB job. e.g. ZHTree")
parser.add_argument("-d", "--date", type=str, help="The task date of CRAB job. e.g. 210412")
parser.add_argument("-dataset", default="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8", help="The large dataset name")
parser.add_argument("-c", default="2018UL", help="The campagin of large dataset, e.g. 2018UL")
args = parser.parse_args()

def checkFolder(path: str) -> None:
    if os.path.exists(path): pass
    else: os.mkdir(path)

def generateScripts(skimScriptSaveFolder: str, skimTTreeSaveFolder: str, dataset: str, campaign: str, macroPath: str, originTTreeFolder: list) -> int:
    checkFolder("{}/{}_{}".format(skimTTreeSaveFolder, dataset, campaign)) # check output skimmed TTree folder
    scanFolder = glob.glob("{}/*.root".format(originTTreeFolder))
    for rootFile in scanFolder:
        scriptSavePath = "{}/reduce_{}.sh".format(skimScriptSaveFolder, scanFolder.index(rootFile))
        with open(scriptSavePath, 'w') as f:
            f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n')
            f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
            f.write('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh\n')
            skimTTreeSavePath = "{}/{}_{}/{}".format(skimTTreeSaveFolder, dataset, campaign, rootFile.split('/')[-1])
            f.write('python3 {} -i {} -o {} -c {}\n'.format(macroPath, rootFile, skimTTreeSavePath, campaign))
        os.chmod(scriptSavePath, 0o755)
        print("Script {} is generated!".format(scriptSavePath))
    return len(scanFolder)

def generateMergeScript(scriptPath: str, skimTTreeSaveFolder: str, dataset: str, campaign: str) -> None:
    scanFolder = glob.glob("{}/{}_{}/*.root".format(skimTTreeSaveFolder, dataset, campaign))
    haddCommand = "hadd {}/{}_{}.root".format(skimTTreeSaveFolder, dataset, campaign)
    for file in scanFolder:
        haddCommand += " {}".format(file)
    with open(scriptPath, 'w') as f:
        f.write(haddCommand)

if __name__ == '__main__':
    t3OriginPath = '/publicfs/cms/user/zhangzhuolin/target_files'
    t3SkimPath = '/publicfs/cms/user/zhangzhuolin/TTreeReducer'
    macroName = '/ntupleSkimmerForCondor.py'
    macroPath = t3SkimPath + macroName
    taskFilePath = t3OriginPath + '/' + args.task + "_" + args.date
    skimFolderPath = t3SkimPath + '/' + args.task + "_" + args.date
    checkResultPath = args.path + "/" + args.task + "_" + args.date
    noCutTreePath = "{}/{}_{}/{}_{}".format(t3OriginPath, args.task, args.date, args.dataset, args.c)

    skimScriptParentFolder = "{}/SkimInCondor".format(checkResultPath)
    checkFolder(skimScriptParentFolder)
    skimScriptDatasetFolder = "{}/{}".format(skimScriptParentFolder, args.dataset)
    checkFolder(skimScriptDatasetFolder)
    mergeScriptSavePath = checkResultPath + "/" + "mergeScript{}.sh".format(args.dataset)
    times = generateScripts(skimScriptDatasetFolder, skimFolderPath, args.dataset, args.c, macroPath, noCutTreePath)
    #generateMergeScript(mergeScriptSavePath, skimFolderPath, args.dataset, args.c)

    print("HTCondor Command: hep_sub {}/{}/reduce_\"%{{ProcId}}\".sh -n {}".format(checkResultPath, args.dataset, times))
    print("The merge script path: {}".format(mergeScriptSavePath))