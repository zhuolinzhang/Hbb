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

def generateScriptOneFile(scriptSavePath: str, skimTTreeSaveFolder: str, dataset: str, campaign: str, macroPath: str, originTTreeFolder: str, task: str, date: str) -> None:
    scanFolder = glob.glob("{}/{}_{}_{}_{}/*.root".format(originTTreeFolder, dataset, task, date, campaign))
    if os.path.exists("{}/{}_{}".format(skimTTreeSaveFolder, dataset, campaign)):
        pass
    else:
        os.mkdir("{}/{}_{}".format(skimTTreeSaveFolder, dataset, campaign))
    with open(scriptSavePath, 'w') as f:
        f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n')
        f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
        f.write('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh\n')
        for rootFile in scanFolder:
            skimTTreeSavePath = "{}/{}_{}/{}".format(skimTTreeSaveFolder, dataset, campaign, rootFile.split('/')[-1])
            f.write('python3 {} -i {} -o {} -c {}\n'.format(macroPath, rootFile, skimTTreeSavePath, campaign))
    os.chmod(scriptSavePath, 0o755)
    print("Script {} is generated!".format(scriptSavePath))

def generateScript(crabResultFolder: str, skimTTreeSaveFolder: str, dataset: str, campaign: str, macroPath: str, scanFolder: list) -> None:
    scriptSaveFolder = "{}/{}".format(crabResultFolder, dataset)
    if os.path.exists("{}/{}_{}".format(skimTTreeSaveFolder, dataset, campaign)):
        pass
    else:
        os.mkdir("{}/{}_{}".format(skimTTreeSaveFolder, dataset, campaign))
    if os.path.exists(scriptSaveFolder):
        pass
    else:
        os.mkdir(scriptSaveFolder)
    for rootFile in scanFolder:
        scriptSavePath = "{}/reduce_{}.sh".format(scriptSaveFolder, scanFolder.index(rootFile))
        with open(scriptSavePath, 'w') as f:
            f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n')
            f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
            f.write('source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.24.06/x86_64-centos7-gcc48-opt/bin/thisroot.sh\n')
            skimTTreeSavePath = "{}/{}_{}/{}".format(skimTTreeSaveFolder, dataset, campaign, rootFile.split('/')[-1])
            f.write('python3 {} -i {} -o {} -c {}\n'.format(macroPath, rootFile, skimTTreeSavePath, campaign))
        os.chmod(scriptSavePath, 0o755)
        print("Script {} is generated!".format(scriptSavePath))

def generateMergeScript(scriptPath: str, skimTTreeSaveFolder: str, dataset: str, campaign: str) -> None:
    scanFolder = glob.glob("{}/{}_{}/*.root".format(skimTTreeSaveFolder, dataset, campaign))
    haddCommand = "hadd {}/{}_{}.root".format(skimTTreeSaveFolder, dataset, campaign)
    for file in scanFolder:
        haddCommand += " {}".format(file)
    with open(scriptPath, 'w') as f:
        f.write(haddCommand)

t3OriginPath = '/publicfs/cms/user/zhangzhuolin/target_files'
t3SkimPath = '/publicfs/cms/user/zhangzhuolin/TTreeReducer'
macroName = '/ntupleSkimmerForCondor.py'
macroPath = t3SkimPath + macroName
taskFilePath = t3OriginPath + '/' + args.task + "_" + args.date
skimFolderPath = t3SkimPath + '/' + args.task + "_" + args.date
checkResultPath = args.path + "/" + args.task + "_" + args.date

#reduceScriptSavePath = checkResultPath + "/" + "reduceScript{}.sh".format(args.dataset)
mergeScriptSavePath = checkResultPath + "/" + "mergeScript{}.sh".format(args.dataset)
scanNtupleFolder = glob.glob("{}/{}_{}_{}_{}/*.root".format(taskFilePath, args.dataset, args.task, args.date, args.c))
generateScript(checkResultPath, skimFolderPath, args.dataset, args.c, macroPath, scanNtupleFolder)
generateMergeScript(mergeScriptSavePath, skimFolderPath, args.dataset, args.c)

print("HTCondor Command: hep_sub {}/{}/reduce_\"%{{ProcId}}\".sh -n {}".format(checkResultPath, args.dataset, len(scanNtupleFolder)))
#print("The skimming script path: {}".format(reduceScriptSavePath))
print("The merge script path: {}".format(mergeScriptSavePath))