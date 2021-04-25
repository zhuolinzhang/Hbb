# Before run this script, you must initialize your VO first.
# This script must be run on the lxslc of IHEP in the python3 environment.

import os
import re

# Check VO
def checkVO():
    if os.path.exists("/tmp/x509up_u12918"):
        pass
    else:
        print("Please activate your VO!")
        os.system("voms-proxy-init -voms cms")

# Read MC Samples and Data list from .txt file
def readLocalList(listFilePath):
    fileList = []
    with open(listFilePath, 'r') as f:
        fileListOrigin = f.readlines()
        for i in fileListOrigin:
            fileList.append(i.rstrip())
    return fileList


def getFileFlag(sampleName, taskName, date, mcOrData):
    findFlag = False
    # my new T2 path
    t2Path = 'gsiftp://ccsrm.ihep.ac.cn/dpm/ihep.ac.cn/home/cms/store/user/zhuolinz'
    if mcOrData == 'mc':
        sampleDirectory = os.popen(
            'gfal-ls -l {0}/{1}'.format(t2Path, sampleName))
    elif mcOrData == 'data':
        sampleDirectory = os.popen('gfal-ls -l {0}/DoubleMuon'.format(t2Path))
    sampleDirectoryList = sampleDirectory.readlines()
    for i in sampleDirectoryList:
        if re.search("{}_{}_{}".format(sampleName, taskName, date), i):
            findFlag = True
            break
    return findFlag

def checkCRABResluts(resultPath, taskName, taskDate):
    resultSavePath = resultPath + '/' + taskName
    if os.path.exists(resultSavePath):
        pass
    else:
        os.mkdir(resultSavePath)
    noOutputMCList = []
    noOutputDataList = []
    mcInputList = readLocalList(resultPath + "/SampleList.txt")
    dataInputList = readLocalList(resultPath + "/DataList.txt")
    mcT2List = []
    dataT2List = []
    # Get MC list and data list in T2
    for i in mcInputList:
        mcFindFlag = getFileFlag(i, taskName, taskFullDate, 'mc')
        if mcFindFlag:
            mcT2List.append(i)
        else:
            noOutputMCList.append(i)
    for i in dataInputList:
        dataFindFlag = getFileFlag(i, taskName, taskFullDate, 'data')
        if dataFindFlag:
            dataT2List.append(i)
        else:
            noOutputDataList.append(i)
    if len(noOutputDataList) == 0 and len(noOutputMCList) == 0:
        print("All CRAB jobs have output!")
    elif len(noOutputMCList) > 0:
        print("There are some MC samples which didn't have output files: ", noOutputMCList)
    elif len(noOutputDataList) > 0:
        print("There are some data which didn't have output files: ", noOutputDataList)
    print("The MC list and data list have been written to ", resultSavePath)
    with open(resultSavePath + '/MCList.txt', 'w') as f:
        for i in mcT2List:
            f.write(i + '\n')
    with open(resultSavePath + '/DataList.txt', 'w') as f:
        for i in dataT2List:
            f.write(i + '\n')
    return mcT2List, dataT2List

if __name__ == '__main__':
    checkVO()
    resultPath = '/publicfs/cms/user/zhangzhuolin/CRABResult'
    taskName = input("Please input the task name: ") # my CRAB job name style: dataset primary name_taskname_date e.g. ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_AddTrigger_210112
    taskFullDate = input("Please input the date (YYMMDD): ")
    #taskYear = '20' + taskFullDate[0:2]
    #taskMonth = taskFullDate[2:4]
    resultTuple = checkCRABResluts(resultPath, taskName, taskFullDate)