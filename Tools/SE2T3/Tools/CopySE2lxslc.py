# Before run this script, you must initialize your VO first.
# This script must be run on the lxslc of IHEP in the python3 environment.

import os
import re
import argparse

# Check VO
def checkVO():
    if os.path.exists("/tmp/x509up_u12918"):
        pass
    else:
        print("Please activate your VO!")
        while not(os.path.exists("/tmp/x509up_u12918")):
            os.system("voms-proxy-init -voms cms")

# Copy files function
def copyFiles(targetDirectory, jobName, dataset, date, mcOrData):
    SEPath = 'gsiftp://ccsrm.ihep.ac.cn/dpm/ihep.ac.cn/home/cms/store/user/zhuolinz' # my new T2 path
    if mcOrData == 'mc':
        jobDateFile = os.popen('gfal-ls {}/{}/{}'.format(SEPath, dataset, jobName))
        datasetPath = SEPath + "/" + dataset + "/" + jobName
    elif mcOrData == 'data':
        jobDateFile = os.popen('gfal-ls {}/DoubleMuon/{}'.format(SEPath, jobName))
        datasetPath = SEPath + "/DoubleMuon/" + jobName
    jobDate = jobDateFile.readline().rstrip()
    os.system('gfal-copy -rf {}/{}/0000 {}/{}'.format(datasetPath, jobDate, targetDirectory, jobName))

def tarFiles(directory, name, date):
    os.chdir(directory)
    os.system('tar -zcvf {}_{}.tar.gz *.root'.format(name, date))
    print("The path of output file is {}/{}_{}.tar.gz".format(directory, name, date))

def main(args):
    crabJobName = args.f
    crabJobNameList = crabJobName.split("_")
    taskDate = crabJobNameList.pop()
    taskName = crabJobNameList.pop()
    primaryDatasetName = crabJobNameList[0]
    if args.type == "data":
        primaryDatasetName = primaryDatasetName.split("/")[1]
    for i in range(1, len(crabJobNameList)):
        primaryDatasetName += "_" + crabJobNameList[i]
    t3Directory = '/publicfs/cms/user/zhangzhuolin/target_files/{}_{}'.format(taskName, taskDate) # my T3 path
    if os.path.exists(t3Directory): pass
    else: os.mkdir(t3Directory)
    copyFiles(t3Directory, crabJobName, primaryDatasetName, taskDate, args.type)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, help="The full CRAB job name of MC sample of data")
    parser.add_argument("--type", type=str, help="MC of Data")
    args = parser.parse_args()
    checkVO()
    main(args)

'''
# Compress all output .root files, print the path
os.chdir(t3Directory)
os.system('tar -zcvf {}_{}.tar.gz *.root'.format(taskName, taskFullDate))
print("************************************")
print("The path of output file is {}/{}_{}.tar.gz".format(t3Directory, taskName, taskFullDate))

if noOutputList != []:
    print("************************************")
    print("There are some MC samples which didn't have output files: ", noOutputList)
'''