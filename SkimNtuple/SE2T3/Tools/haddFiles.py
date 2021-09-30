# This script can be executed independently
import os
import argparse
import shutil

# Generate HTCondor scripts, this function doesn't called in the main function
def generateScripts(savePath: str, sourcePath: str, jobName: str, scriptNum: str, datasetType: str, campaign: str) -> None:
    if os.path.exists(savePath): pass
    else: os.mkdir(savePath)
    fileName = 'haddJobSubmit_{}_{}.sh'.format(campaign, scriptNum)
    with open(savePath +"/" + fileName, 'w') as f:
        f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n')
        f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
        if datasetType == 'mc':
            f.write('python3 {}/haddFiles.py --job {} --type mc -c {}\n'.format(sourcePath, jobName, campaign))
        elif datasetType == 'data':
            f.write('python3 {}/haddFiles.py --job {} --type data -c {}\n'.format(sourcePath, jobName, campaign))
    os.chmod(savePath +"/" + fileName, 0o755)
    print('*' * 70)
    print("Script {} is generated!".format(fileName))
    print('*' * 70)

# hadd root files
def haddFiles(targetDirectory: str, jobName: str, datasetName: str, optimizeFlag: bool, campagin: str) -> None:
    directoryList = os.listdir('{}/{}'.format(targetDirectory, jobName))
    if len(directoryList) > 1:
        haddCommand = 'hadd -f {0}/{1}_{2}.root'.format(targetDirectory, datasetName, campagin) # -f force
        for i in directoryList:
            haddCommand += ' {}/{}/{}'.format(targetDirectory, jobName, i)
        print('#' * 70)
        print("{} is starting merging.".format(jobName))
        os.system(haddCommand)
        print('#' * 70)
        if optimizeFlag:
            shutil.rmtree('{}/{}'.format(targetDirectory, jobName)) # remove source .root files
            print("The folder {}/{} has been deleted!".format(targetDirectory, jobName))
    elif len(directoryList) == 1:
        os.system('cp {0}/{2}/*.root {0}/{1}_{3}.root'.format(targetDirectory, datasetName, jobName, campagin))
        print("{} does not need to merge. It is copied to target path!".format(jobName))
        if optimizeFlag: 
            shutil.rmtree('{}/{}'.format(targetDirectory, jobName))
            print("The folder {}/{} has been deleted!".format(targetDirectory, jobName))
    else: print("Your job {} does not have any output, please check it!".format(jobName))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", help="Delete all source files", action='store_true')
    parser.add_argument("--job", type=str, help="The full CRAB job name") # e.g. DoubleMuonPrompt2018D_AddTrigger_210112
    parser.add_argument("-f", type=str, default="/publicfs/cms/user/zhangzhuolin/target_files",help='T3 target_files folder path') # /publicfs/cms/user/zhangzhuolin/target_files
    parser.add_argument("--type", type=str, help="mc or data")
    parser.add_argument("-c", help="The campaign of datasets")
    args = parser.parse_args()
    jobNameList = args.job.split("_")
    taskDate = jobNameList.pop()
    taskName = jobNameList.pop()
    datasetName = jobNameList[0]
    # Get the dataset name of MC. The primary name of MC samples has lots of underlines, so this loop is needed.
    if args.type == 'mc':
        for i in range(1, len(jobNameList)):
            datasetName += "_" + jobNameList[i]
    t3Directory = args.f + '/{}_{}'.format(taskName, taskDate) # my T3 path
    haddFiles(t3Directory, args.job, datasetName, args.clean, args.c)
