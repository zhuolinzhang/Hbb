import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", help="The JSON file path")
args = parser.parse_args()

def findNewerULWithPattern(dbsName: str, oldPattern: str, newPattern: str) -> str:
	newDbsName = ""
	if newPattern in dbsName:
		print("The dataset is the latest!")
		newDbsName = dbsName
	else:
		hypotheticalDbs = dbsName.replace(oldPattern, newPattern)
		queryResult = os.popen('dasgoclient -query="dataset={}"'.format(hypotheticalDbs))
		queryResultList = queryResult.readlines()
		if len(queryResultList) == 0:
			print("Can't find newer {} version, this dataset is the latest.".format(newPattern))
			newDbsName = dbsName
		else:
			newDbsName = queryResultList[0].rstrip()
			print("{}: {}".format(newPattern, newDbsName))
	return newDbsName

def findNewerUL(dbsName: str, campaign: str) -> str:
	if "RunIISummer20" in dbsName:
		newDatasetDbs = findNewerULWithPattern(dbsName, "MiniAOD", "MiniAODv2")
	else: 
		newDatasetDbs = findNewerULWithPattern(dbsName, "RunIISummer19UL", "RunIISummer20UL")
		if "2016APV" in campaign:
			newDatasetDbs = findNewerULWithPattern(newDatasetDbs, "MiniAODAPV", "MiniAODAPVv2")
		else: newDatasetDbs = findNewerULWithPattern(newDatasetDbs, "MiniAOD", "MiniAODv2")
	return newDatasetDbs

datasetList = []
with open(args.f, 'r') as f:
	datasetList = json.load(f)

campaignULDict = {"2016APV": "16", "2016": "16", "2017": "17", "2018": "18"}
for dataset in datasetList:
	print("{} campaign: {} category: {}".format(dataset["primaryName"], dataset["campaign"], dataset["category"]))
	if dataset["category"] == 'data':
		print("The script will not check data samples because every data sample is in UL campaign.")
		continue
	else:
		if "UL" in dataset["campaign"]:
			print("The dataset is in UL campaign, now will only check the MiniAOD version.")
			newDatasetDbs = findNewerUL(dataset["dasName"], dataset["campaign"])
		else:
			wildcartQueryList = []
			wildcartQuery = os.popen('dasgoclient -query="dataset=/{}/*/MINIAODSIM"'.format(dataset["primaryName"]))
			wildcartQueryList = wildcartQuery.readlines()
			datasetYear = dataset["campaign"].rstrip("UL").rstrip("ReReco")
			for result in wildcartQueryList:
				if "RunIISummer19UL{}".format(campaignULDict[datasetYear]) in result or "RunIISummer20UL{}".format(campaignULDict[datasetYear]) in result:
					print("Find UL campaign of {}".format(dataset["primaryName"]))
					newDatasetDbs = findNewerUL(result.rstrip(), "{}UL".format(datasetYear))