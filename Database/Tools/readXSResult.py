import glob
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="The path of input .json file")
parser.add_argument("-o", help="The path of output .json file, if don't input this argument, the output path is same as input path")
args = parser.parse_args()

outPutPath = ''
if args.o == None: outPutPath = args.i
else: outPutPath = args.o

def readXS(fileName: str) -> float:
	xsecLog = []
	xsLineList = []
	findXSFlag = False
	with open(fileName, 'r') as f:
		xsecLog = f.readlines()
	for line in reversed(xsecLog):
		if 'final cross section' in line:
			xsLineList = line.split()
			findXSFlag = True
			break
	if findXSFlag:
		return float(xsLineList[-4])
	else: 
		print("{} dosen't have XS result!".format(fileName))
		return 0

def readPrimaryName(fileName: str) -> str:
	return fileName.strip('xsec_').rstrip('.log')

datasetList = []
with open(args.i, 'r') as f:
	datasetList = json.load(f)

xsecLogFileList = glob.glob("xsec_*.log")
for i in xsecLogFileList:
	xs = readXS(i)
	primaryName = readPrimaryName(i)
	if xs != 0: 
		print("Read {}".format(primaryName))
		for datasetDict in datasetList:
			if primaryName in datasetDict.values():
				datasetDict["xs"] = xs
				break
with open(outPutPath, 'w') as fOut:
	json.dump(datasetList, fOut, indent=4)