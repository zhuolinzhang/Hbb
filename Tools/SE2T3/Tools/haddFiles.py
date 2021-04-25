import os
import re
import argparse
import shutil

def haddFiles(targetDirectory, jobName, datasetName, optimizeFlag=None):
    directoryList = os.listdir('{}/{}'.format(targetDirectory, jobName))
    if len(directoryList) > 1:
        haddCommand = 'hadd -f {0}/{1}.root'.format(targetDirectory, datasetName)
        for i in directoryList:
            haddCommand += ' {}/{}/{}'.format(targetDirectory, jobName, i)
        print("{} is starting merging.".format(jobName))
        os.system(haddCommand)
        if optimizeFlag == "skim": 
            shutil.rmtree('{}/{}'.format(targetDirectory, jobName))
            print("The folder {}/{} has been deleted!".format(targetDirectory, jobName))
    elif len(directoryList) == 1:
        os.system('cp {0}/{2}/*.root {0}/{1}.root'.format(targetDirectory, datasetName, jobName))
        print("{} does not need to merge. It is copied to target path!".format(jobName))
        if optimizeFlag == "skim": 
            shutil.rmtree('{}/{}'.format(targetDirectory, jobName))
            print("The folder {}/{} has been deleted!".format(targetDirectory, jobName))
    else: print("Your job {} does not have any output, please check it!".format(jobName))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", type=str, help="Input skim to delete all source files")
    parser.add_argument("--job", type=str, help="The full CRAB job name")
    parser.add_argument("-f", type=str, default="/publicfs/cms/user/zhangzhuolin/target_files",help='T3 target_files folder path') # /publicfs/cms/user/zhangzhuolin/target_files
    args = parser.parse_args()
    jobNameList = args.job.split("_")
    taskDate = jobNameList.pop()
    taskName = jobNameList.pop()
    datasetName = jobNameList[0]
    t3Directory = args.f + '/{}_{}'.format(taskName, taskDate) # my T3 path
    haddFiles(t3Directory, args.job, datasetName, args.o)