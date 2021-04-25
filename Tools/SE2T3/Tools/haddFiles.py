import os
import re
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-o", type=str, help="Input skim to delete all source files")
parser.add_argument("--job", type=str, help="The full CRAB job name")
parser.add_argument("-f", type=str, help='T3 target folder path')
args = parser.parse_args()

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
    t3Directory = '/publicfs/cms/user/zhangzhuolin/target_files/{}'.format(args.job) # my T3 path
    jobNameList = args.job.split("_")
    for i in range(0,2):
        jobNameList.pop()
    datasetName = jobNameList[0]
    for i in range(1, len(jobNameList)):
        datasetName += "_" + jobNameList[i]
    haddFiles(t3Directory, args.job, datasetName, args.o)