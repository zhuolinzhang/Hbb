# This script will 
# 1 - check the number of events for each dataset and correct it. Then, it will calculate the right normalization factor
# 2 - check the primary name
# 3 - check the scale factor
# This script MUST be run on the LXPLUS or lxslc(IHEP)

import argparse
import os
import json

parse = argparse.ArgumentParser()
parse.add_argument("--lumi", type=float, default=59.83, help="The integrated luminosity of data (/fb)")
parse.add_argument("-i", type=str, help="The path of input json file")
parse.add_argument("-o", type=str, default=None, help="The path of output json file, the default path is same as the input path")
parse.add_argument("-t", type=str, default='factor', help="The factor which you want to check")
args = parse.parse_args()

def checkVO():
    if os.path.exists("/tmp/x509up_u12918"): # for lxpuls(CERN), /tmp/x509up_u132269
        pass
    else:
        print("Please activate your VO!")
        while not(os.path.exists("/tmp/x509up_u12918")):
            os.system("voms-proxy-init -voms cms")

checkVO()
databaseList = []
newDatabaseList = []
with open(args.i, 'r') as databaseJson:
    databaseList = json.load(databaseJson)
print('*' * 60)
for datasetDict in databaseList:
    newDatasetDict = datasetDict
    nEvents = datasetDict["nEvents"]
    print("Read {}".format(datasetDict["primaryName"]))
    for key, value in datasetDict.items():
        if key == "primaryName":
            newPrimaryName = datasetDict["dasName"].split('/')[1]
            if value == newPrimaryName: pass
            else: 
                print("The primary_name is wrong. Correct it!")
                newDatasetDict["primaryName"] = newPrimaryName
        if key == "dasName":
            f = os.popen('dasgoclient -query="summary dataset={}"'.format(value))
            dasSummary = f.readline()
            dasSummaryList = dasSummary.split(",")
            for i in dasSummaryList:
                if "nevents" in i:
                    nEvents = int(i.split(":")[-1])
            if datasetDict["nEvents"] == nEvents:
                continue
            else:
                print("The nevnets is wrong!\tlocal = {}\tdas = {}".format(datasetDict["nEvents"], nEvents))
                newDatasetDict["nEvents"] = nEvents
                newDatasetDict[args.t] = args.lumi / ((nEvents / datasetDict["xs"]) / 1000)
        if key == "nEvents":
            if value == nEvents:
                factor = args.lumi / ((nEvents / datasetDict["xs"]) / 1000)
                if datasetDict[args.t] == factor: continue
                else:
                    print("The scale factor to {} /fb is wrong!\tnow = {}\tcalculate = {}".format(args.lumi, datasetDict[args.t], factor))
                    newDatasetDict[args.t] = factor
        
    newDatabaseList.append(newDatasetDict)
    print('*' * 60)
        
outputPath = args.o
if args.o == None: outputPath = args.i
with open(outputPath, 'w') as newJson:
    json.dump(newDatabaseList, newJson, indent=4)
