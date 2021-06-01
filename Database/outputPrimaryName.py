import json
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-i", help="Path of input json file")
parse.add_argument("-o", help="Path of output .txt file")
args = parse.parse_args()

inputList = []
primaryNameList = []

with open(args.i, 'r') as f:
    inputList = json.load(f)

for datasetDict in inputList:
    primaryNameList.append(datasetDict["primary_name"] + '\n')

with open(args.o, 'w') as fout:
    for i in primaryNameList:
        fout.write(i)