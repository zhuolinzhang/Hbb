# This script can only be used to create a new JSON file

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="The path of input .txt file")
parser.add_argument("-o", help="The path of output .json file")
args = parser.parse_args()

def writeJSONItem(name: str) -> dict:
	datasetDict = {"primary_name": 0, "nevents": 0, "xsection": 0, "factor": 0, "factor_IsoMu20": 0, "dasname": 0}
	primaryName = name.split('/')[1]
	datasetDict["primary_name"] = primaryName
	datasetDict["dasname"] = name
	return datasetDict

jsonList = []
datasetList = []
with open(args.i, 'r') as f:
	for line in f:
		datasetList.append(line.rstrip())
for i in datasetList:
	 datasetInfo = writeJSONItem(i)
	 jsonList.append(datasetInfo)

with open(args.o, 'w') as fOut:
	json.dump(jsonList, fOut, indent=4)