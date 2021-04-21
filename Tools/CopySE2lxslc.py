# Before run this script, you must initialize your VO first.
# This script must be run on the lxslc of IHEP in the python3 environment.

import os
import re

# Check VO
if os.path.exists("/tmp/x509up_u12918"): pass
else:
    print("Please activate your VO!")
    os.system("voms-proxy-init -voms cms")

# Copy files function
def copyFiles(SEPath, targetDirectory, name, dataset, year, month, fullDate, mcOrData):
    datasetPath = os.popen('gfal-ls -l {}/{} --full-time | grep {}-{}-[0-9][0-9]'.format(SEPath, dataset, year, month))
    datasetPathPrimaryList = datasetPath.readlines()
    checkFlag = True
    for j in datasetPathPrimaryList:
        if re.search('_{}_{}'.format(name, fullDate), j):
            checkFlag = False
            taskFullName = j.split()[-1]
            jobDateFile = os.popen('gfal-ls {}/{}/{}'.format(SEPath, dataset, taskFullName))
            jobDate = jobDateFile.readline().rstrip()
            os.system('gfal-copy -r {}/{}/{}/{}/0000 {}/{}'.format(SEPath, dataset, taskFullName, jobDate, targetDirectory, taskFullName))
            newDirectoryList = os.listdir('{}/{}'.format(targetDirectory,taskFullName))
            if mcOrData == 'mc':
                newFileName = dataset
            elif mcOrData == 'data':
                newFileName = taskFullName.split('_')[0]
            if len(newDirectoryList) > 1:
                os.system('hadd {0}/{1}.root {0}/{2}/*.root'.format(targetDirectory, newFileName, taskFullName))
            else:
                os.system('cp {0}/{2}/*.root {0}/{1}.root'.format(targetDirectory, newFileName, taskFullName))
    return checkFlag

mySEPath = 'gsiftp://ccsrm.ihep.ac.cn/dpm/ihep.ac.cn/home/cms/store/user/zhuolinz' # my new T2 path
print("If your VO is not valid, you can input voinit to initialize VO")
taskName = input("Please input the task name: ") # my CRAB job name style: dataset primary name_taskname_date e.g. ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_AddTrigger_210112
taskFullDate = input("Please input the date (YYMMDD): ")
taskYear = '20' + taskFullDate[0:2]
taskMonth = taskFullDate[2:4]

t3Directory = '/cms/user/zhangzhuolin/target_files/{}_{}'.format(taskName, taskFullDate) # my T3 path
os.system('mkdir {}'.format(t3Directory))
homeDirectory = os.popen('gfal-ls -l {} --full-time | grep {}-{}-[0-9][0-9]'.format(mySEPath, taskYear, taskMonth))
mcDirectoryList = []
noOutputList = []
dataDirectoryList = []
homeDirectoryPrimaryList = homeDirectory.readlines()
for i in homeDirectoryPrimaryList:
    mcDirectoryList.append(i.split()[-1])
for i in mcDirectoryList:
    if re.search('TeV', i):
        continue
    else:
        dataDirectoryList.append(i)
for i in dataDirectoryList:
    mcDirectoryList.remove(i)

for datasetName in mcDirectoryList:
    noOutputFlag = copyFiles(mySEPath, t3Directory, taskName, datasetName, taskYear, taskMonth, taskFullDate, 'mc')
    if noOutputFlag:
        noOutputList.append(datasetName)

for datasetName in dataDirectoryList:
    noOutputFlag = copyFiles(mySEPath, t3Directory, taskName, datasetName, taskYear, taskMonth, taskFullDate, 'data')

# Compress all output .root files, print the path
os.chdir(t3Directory)
os.system('tar -zcvf {}_{}.tar.gz *.root'.format(taskName, taskFullDate))
print("************************************")
print("The path of output file is {}/{}_{}.tar.gz".format(t3Directory, taskName, taskFullDate))

if noOutputList != []:
    print("************************************")
    print("There are some MC samples which didn't have output files: ", noOutputList)