# This script can only be used to create a new JSON file

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="The path of input .txt file")
parser.add_argument("-o", help="The path of output .json file")
parser.add_argument("-t", help="Type of json file, data or mc")
args = parser.parse_args()

def checkCampaign(dasName : str, mcOrData: str) -> str:
	year = ''
	legacy = ''
	if mcOrData == "mc":
		if 'upgrade2018' in dasName: year = '2018'
		elif 'mc2017' in dasName: year = '2017'
		elif 'mcRun2' in dasName: 
			year = '2016'
			if "APV" in dasName:
				year = "2016APV"
		else: raise SystemError("Cannot read year from the dataset!")
		if 'Summer19UL' in dasName or 'Summer20UL' in dasName:
			legacy = 'UL'
		else: legacy = 'ReReco'
	elif mcOrData == "data":
		if '2018' in dasName: year = '2018'
		elif '2017' in dasName: year = '2017'
		elif '2016' in dasName: 
			year = '2016'
			if 'HIPM' in dasName: year = '2016APV'
			legacy = 'UL'
	else: raise SystemExit("The campagin of dataset {} cannot be read. Please check it!".format(dasName))
	fullCampaign = year + legacy
	return fullCampaign

def readDatasetCategory(name: str) -> str:
	category = 'none'
	matchDict = {'ZH_HToBB': 'zh', 'TTTo': 'tt', 'channel': 'st', 'ZZ': 'zz', 'QCD': 'qcd', 'JetsToLL': 'zjets', 'DoubleMuon': 'data'}
	for key, value in matchDict.items():
		if key in name:
			category = value
			continue
	return category

def writeJSONItem(name: str, mcOrData: str) -> dict:
	if mcOrData == 'mc': 
		datasetDict = {"primaryName": 0, "dasName": 0, "campaign": 0, "category": 0, "nEvents": 1, "xs": 0, "factor": 1}
		primaryName = name.split('/')[1]
		datasetDict["primaryName"] = primaryName
		datasetDict["dasName"] = name
		datasetDict["campaign"] = checkCampaign(name, mcOrData)
		datasetDict["category"] = readDatasetCategory(name)
		if datasetDict["category"] == 'none': raise SystemExit("This dataset can't be categorized, please check the name of dataset or s this script.")
		if "2017" in datasetDict["campaign"] or "2016" in datasetDict["campaign"]:
			datasetDict["factorIsoMu20"] = 1
		if "2016" in datasetDict['campaign']:
			datasetDict['factorMu17'] = 1
	elif mcOrData == 'data':
		datasetDict = {"primaryName": 0, "dasName": 0, "campaign": 0, "category": 0}
		datasetDict['primaryName'] = "DoubleMuon" + name.split("/")[2].split("-")[0].strip("Run")
		datasetDict['dasName'] = name
		datasetDict["campaign"] = checkCampaign(name, mcOrData)
		datasetDict["category"] = readDatasetCategory(name)
		if datasetDict["category"] == 'none': raise SystemExit("This dataset can't be categorized, please check the name of dataset or s this script.")

	return datasetDict

jsonList = []
datasetList = []
with open(args.i, 'r') as f:
	for line in f:
		datasetList.append(line.rstrip())
for i in datasetList:
	 datasetInfo = writeJSONItem(i, args.t)
	 jsonList.append(datasetInfo)

with open(args.o, 'w') as fOut:
	json.dump(jsonList, fOut, indent=4)