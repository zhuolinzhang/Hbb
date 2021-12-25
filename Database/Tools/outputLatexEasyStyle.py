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
    rowList.append(datasetDict["dasName"].replace("_", "\_"))
    rowList.append("{:.2f}".format(datasetDict["nEvents"] * datasetDict["factorMu17"]))
    rowList.append(datasetDict["xs"])
    outPutDict[datasetDict["primaryName"]] = rowList
    
with open(args.o, 'w') as fout:
    for key, value in outPutDict.items():
        for i in value:
            if i != value[-1]:
                fout.write(str(i) + ' & ')
            else: 
                fout.write(str(i) + '\\\\' +'\n')
