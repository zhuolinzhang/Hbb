import json
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", help="The search category, c or n")
parser.add_argument("-w", help="The key word")
args = parser.parse_args()

dataSetFileList = glob.glob("../MCInfo*.json")
totalEvent = 0
totalXs = []
searchTerm = 'category'
if args.c == 'n':
	searchTerm = 'dasName'

for file in dataSetFileList:
	dataSetList = []
	totalXsNum = 0
	with open(file) as f:
		dataSetList = json.load(f)
	for dataSet in dataSetList:
		if args.w in dataSet[searchTerm]:
			totalEvent += dataSet['factor'] * dataSet['nEvents']
			totalXsNum += dataSet['xs']
	totalXs.append(totalXsNum)

print("Result of {} in all data sets: XS: {}, nEvents: {:.3e}".format(args.w, totalXs, totalEvent))