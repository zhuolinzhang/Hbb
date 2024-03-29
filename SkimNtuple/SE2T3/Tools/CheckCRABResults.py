# Before run this script, you must initialize your VO first.
# This script must be run on the lxslc of IHEP in the python3 environment.

import os
import argparse
import json
from typing import Dict, List, Tuple

# Check VO is activated. But if the VO is invalid, this function doesn't work. I will update to fix this
# bug in the future.
def checkVO() -> None:
    if os.path.exists("/tmp/x509up_u12918"):
        pass
    else:
        print("Please activate your VO!")
        while not(os.path.exists("/tmp/x509up_u12918")):
            os.system("voms-proxy-init -voms cms")

# Read MC Samples and Data list from .json file. 
# We can modify the .json file to decide which MC sample of data is needed to check.
def readDatabaseList(listFilePath: str) -> List[Dict]:
    jsonList = []
    datasetInputList = []
    with open(listFilePath, 'r') as f:
        jsonList = json.load(f)
    for dataset in jsonList:
        skimDatasetDict = {}
        skimDatasetDict["primaryName"] = dataset["primaryName"]
        skimDatasetDict["category"] = dataset["category"]
        skimDatasetDict["campaign"] = dataset["campaign"]
        datasetInputList.append(skimDatasetDict)
    return datasetInputList

# Return the result whether the dataset is found in the CRAB results.
# return a bool value
def getFileFlag(sampleName: str, taskName: str, date: str, mcOrData: str) -> bool:
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
        if "{}_{}_{}".format(sampleName, taskName, date) in i:
            findFlag = True
            break
    return findFlag

def checkOutput(path: str) -> None:
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)

def queryCRABResults(resultPath: str, taskName: str, taskDate: str, datasetListPath: List[str]) -> Dict[str, Dict[str, List[str]]]:
    resultSavePath = "{}/{}_{}".format(resultPath, taskName, taskDate)
    checkOutput(resultSavePath)
    inputList = []
    queryResult = {"mc": {}, "data": {}} # e.g. {"mc": {"2018UL": ["DYJets...", ...], "2018ReReco": ["ZH_HToBB_ZToLL", ...]}, "data": {...}}
    for datasetFile in datasetListPath:
        inputList += readDatabaseList(datasetFile)
    for dataset in inputList:
        if dataset["category"] == "data":
            datasetTag = "data"
        else: datasetTag = "mc"
        if getFileFlag(dataset["primaryName"], taskName, taskDate, datasetTag):
            print("Find dataset Name: {}, Campaign: {}, Category: {}".format(dataset["primaryName"], dataset["campaign"], datasetTag))
            if dataset["campaign"] in queryResult[datasetTag]:
                queryResult[datasetTag][dataset["campaign"]].append(dataset["primaryName"])
            else:
                queryResult[datasetTag][dataset["campaign"]] = [dataset["primaryName"]]
        else: print("!!! Can't find dataset Name: {}, Campaign: {}, Category: {}".format(dataset["primaryName"], dataset["campaign"], datasetTag))
    with open("{}/QueryResult.json".format(resultSavePath), 'w') as f:
        json.dump(queryResult, f, indent=4)
    return queryResult

'''
# The main function
def checkCRABResults(resultPath: str, taskName: str, taskDate: str, years: str, datasetListPath=None, customDatasetPathData=False) -> Tuple[dict]:
    resultSavePath = resultPath + '/' + taskName + "_" + taskDate # The folder that saves the .txt file which include primary names of dataset
    checkOutput(resultSavePath)
    noOutputMCList = []
    noOutputDataList = []
    if datasetListPath == None:
        # When the dataset is changed, this file should also changed.
        mcInputDict = readLocalList("/cms/user/zhangzhuolin/Database/Stable/MCInfo{}.json".format(years))
        # When the dataset is changed, this file should also changed.
        dataInputDict = readLocalList("/cms/user/zhangzhuolin/Database/Stable/DataInfo{}.json".format(years))
    if datasetListPath != None:
        if customDatasetPathData:
            mcInputDict = []
            dataInputDict = readLocalList(datasetListPath)
        else:
            mcInputDict = readLocalList(datasetListPath)
            dataInputDict = []

    mcT2Dict = copy.deepcopy(mcInputDict)
    dataT2Dict = copy.deepcopy(dataInputDict)
    # Get MC list and data list in T2
    for campagin, datasetList in mcInputDict.items():
        for i in datasetList:
            mcFindFlag = getFileFlag(i, taskName, taskDate, 'mc')
            if mcFindFlag:
                pass
            else:
                noOutputMCList.append(i)
                mcT2Dict[campagin].remove(i)
    for campagin, datasetList in dataInputDict.items():
        for i in datasetList:
            dataFindFlag = getFileFlag(i, taskName, taskDate, 'data')
            if dataFindFlag:
                pass
            else:
                noOutputDataList.append(i)
                dataT2Dict[campagin].remove(i)
    if len(noOutputDataList) == 0 and len(noOutputMCList) == 0:
        print('*' * 70)
        print("All CRAB jobs have output!")
        print('*' * 70)
    elif len(noOutputMCList) > 0:
        print('*' * 70)
        print("There are some MC samples which didn't have output files: ", noOutputMCList)
        print('*' * 70)
    elif len(noOutputDataList) > 0:
        print('*' * 70)
        print("There are some data which didn't have output files: ", noOutputDataList)
        print('*' * 70)
    print('#' * 70)
    print("The MC list and data list have been written to ", resultSavePath)
    print('#' * 70)
    with open(resultSavePath + '/MCList.json', 'w') as f: # Save MC samples which have output in a .txt file
        json.dump(mcT2Dict, f, indent=4)
    with open(resultSavePath + '/DataList.json', 'w') as f: # Save data which have output in a .txt file
        json.dump(dataT2Dict, f, indent=4)
    return mcT2Dict, dataT2Dict # return a tuple
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="The date of CRAB job (YYMMDD)")
    parser.add_argument("-t", help="The name of CRAB task (e.g. ZHTreeUL18)")
    parser.add_argument("-y", help="Years of datasets")
    args = parser.parse_args()
    checkVO()
    resultPath = '/publicfs/cms/user/zhangzhuolin/CRABResult'
    #resultTuple = checkCRABResults(resultPath, args.t, args.d, args.y)