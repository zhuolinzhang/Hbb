# This script can only be used to create a new JSON file

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="The path of input .txt file")
parser.add_argument("-o", help="The path of output .json file")
args = parser.parse_args()

def checkCampaign(dasName : str) -> str:
	year = ''
	legacy = ''
	if 'upgrade2018' in dasName: year = '2018'
	elif 'mc2017' in dasName: year = '2017'
	elif 'mcRun2' in dasName: year = '2016'
	else: raise SystemError("Cannot read year from the dataset!")
	if 'Summer19UL' in dasName or 'Summer20UL' in dasName:
		legacy = 'UL'
	else: legacy = 'ReReco'
	return year + legacy

def writeJSONItem(name: str) -> dict:
	datasetDict = {"primaryName": 0, "dasName": 0, "campaign": 0, "nEvents": 1, "xs": 0, "factor": 1, "factorIsoMu20": 1}
	primaryName = name.split('/')[1]
	datasetDict["primaryName"] = primaryName
	datasetDict["dasName"] = name
	datasetDict["campaign"] = checkCampaign(name)
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