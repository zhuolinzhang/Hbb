# This module can be executed independently.
# This script must be run on the lxslc of IHEP in the python3 environment.

import os
import argparse
import tarfile
import glob

# Check VO is activated. But if the VO is invalid, this function doesn't work. I will update to fix this
# bug in the future.
def checkVO() -> None:
    if os.path.exists("/tmp/x509up_u12918"):
        pass
    else:
        print("Please activate your VO!")
        while not(os.path.exists("/tmp/x509up_u12918")):
            os.system("voms-proxy-init -voms cms")

# Copy files from T2 to T3
def copyFiles(targetDirectory: str, jobName: str, dataset: str, mcOrData: str, campaign: str) -> None:
    SEPath = "gsiftp://ccsrm.ihep.ac.cn/dpm/ihep.ac.cn/home/cms/store/user/zhuolinz" # my new T2 path
    if mcOrData == "mc":
        jobDateFile = os.popen("gfal-ls {}/{}/{}".format(SEPath, dataset, jobName))
        datasetPath = SEPath + '/' + dataset + '/' + jobName
    elif mcOrData == "data":
        jobDateFile = os.popen("gfal-ls {}/DoubleMuon/{}".format(SEPath, jobName))
        datasetPath = SEPath + "/DoubleMuon/" + jobName
    jobDate = jobDateFile.readline().rstrip()
    fileAutoSaveFile = os.popen("gfal-ls {}".format(datasetPath))
    fileAutoSaveList = [i.rstrip() for i in fileAutoSaveFile.readlines()]
    if len(fileAutoSaveList) == 1:
        os.system('gfal-copy -rf {}/{}/0000 {}/{}_{}'.format(datasetPath, jobDate, targetDirectory, jobName, campaign))
    else: 
        print("Warning: the auto save of files is larger than 1!")
        for i in fileAutoSaveList:
            os.system('gfal-copy -rf {}/{}/{} {}/{}_{}'.format(datasetPath, jobDate, i, targetDirectory, jobName, campaign, i))

# Tar root files. This function isn't suggested to use. Because some files are NOT merged in this stage.
def tarFiles(directory: str, name: str, date: str) -> None:
    os.chdir(directory)
    rootFiles = glob.glob("./*.root")
    tarball = tarfile.open("./{}_{}".format(name,date), "w|gz")
    for file in rootFiles:
        tarball.add(file)
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
    copyFiles(t3Directory, crabJobName, primaryDatasetName, taskDate, args.type, args.c)
    if args.tar:
        tarFiles(t3Directory, taskName, taskDate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, help="The full CRAB job name of MC sample or data")
    parser.add_argument("-t", "--type", type=str, help="MC or Data")
    parser.add_argument("-c", default="2018UL", help="The campagin of dataset e.g. 2018UL")
    parser.add_argument("-tar", action="store_true", help="Compress all .root files")
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