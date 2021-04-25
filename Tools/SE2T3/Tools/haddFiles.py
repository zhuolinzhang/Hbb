import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", type=str, help="Input skim to delete all hadd root source files")
parser.add_argument("--job", type=str, help="The full CRAB job name")
parser.add_argument("-f", type=str, help='T3 target folder path')
args = parser.parse_args()

def haddFiles(targetDirectory, jobName, optimizeFlag=None):
    directoryList = os.listdir('{}/{}'.format(targetDirectory, jobName))
    if len(newDirectoryList) > 1:
        haddCommand = 'hadd -f {0}/{1}.root'.format(targetDirectory, dataset)
        for i in newDirectoryList:
            haddCommand += ' {}/{}/{}'.format(targetDirectory, jobName, i)
        print("{} is starting merging.".format(jobName))
        os.system(haddCommand)
        if optimizeFlag == "skim": 
            shutil.rmtree('{}/{}'.format(targetDirectory, jobName))
            print("The folder {}/{} has been deleted!".format(targetDirectory, jobName))
    elif len(newDirectoryList) == 1:
        os.system('cp {0}/{2}/*.root {0}/{1}.root'.format(targetDirectory, dataset, jobName))
        print("{} does not need to merge. It is copied to target path!".format(jobName))
        if optimizeFlag == "skim": 
            shutil.rmtree('{}/{}'.format(targetDirectory, jobName))
            print("The folder {}/{} has been deleted!".format(targetDirectory, jobName))
    else: print("Your job {} does not have any output, please check it!".format(jobName))

if __name__ == '__main__':
    t3Directory = '/publicfs/cms/user/zhangzhuolin/target_files/{}'.format(jobName) # my T3 path
    haddFiles(t3Directory, parser.job, args.o)