import json
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-i", help="Path of input json file")
parse.add_argument("-o", help="Path of output .txt file")
args = parse.parse_args()

inputList = []
outPutDict = {}

with open(args.i, 'r') as f:
    inputList = json.load(f)

for datasetDict in inputList:
    rowList = []
    primaryName = datasetDict["primaryName"].replace("_", "\_").strip("\\")
    if "ReReco" in datasetDict["campaign"]:
        primaryName = "\\textcolor{{red}}{{ {} }}".format(primaryName)
    #rowList.append("{:.2f}".format(datasetDict["nEvents"] * datasetDict["factorMu17"]))
    rowList.append(primaryName)
    rowList.append(datasetDict["nEvents"])
    rowList.append(datasetDict["xs"])
    if "factorIsoMu20" in datasetDict:
        rowList.append("{:.3e}".format(datasetDict["factorIsoMu20"]))
    elif "factorMu17Mu8" in datasetDict:
        rowList.append("{:.3e}".format(datasetDict["factorMu17Mu8"]))
    elif "factorMu17" in datasetDict:
        rowList.append("{:.3e}".format(datasetDict["factorMu17"]))
    outPutDict[datasetDict["primaryName"]] = rowList
    
with open(args.o, 'w') as fout:
    for key, value in outPutDict.items():
        for i in value:
            if i != value[-1]:
                fout.write(str(i) + ' & ')
            else: 
                fout.write(str(i) + '\\\\' +'\n')
