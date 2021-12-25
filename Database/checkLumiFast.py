import json
import glob

fileList = glob.glob("MCInfo*.json")
for file in fileList:
    print(file.split("/")[-1])
    datasetList = []
    with open(file, 'r') as f:
        datasetList = json.load(f)
    for d in datasetList:
        lumi = d["nEvents"] / (d["xs"] * 1000) * d["factor"]
        print(lumi)
