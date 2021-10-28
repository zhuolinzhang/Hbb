import blindTree
import categorizeTree
import argparse
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument("-sbPath", default= "./sideband", help="The path of sideband samples")
parser.add_argument("-srPath", default= "./sr", help="The path of signal region samples")
parser.add_argument("-srOutput", default="./SRcategorizedTree", help="The path of output hists")
parser.add_argument("-sbOutput", default="./SBcategorizedTree", help="The path of output hists")
parser.add_argument("-tree", default="ZHCandidates", help="The name of TTree")
parser.add_argument("-source", default="./source", help="The path of source")
parser.add_argument("-y", default="run2", help="The year of datasets")
args = parser.parse_args()

def checkOutput(path: str) -> None:
	if os.path.exists(path): pass
	else: os.mkdir(path)
if args.y == "run2":
	rootFilesList = glob.glob("{}/*.root".format(args.source))
else:
	rootFilesList = glob.glob("{}/*{}[RU]*.root".format(args.source, args.y))
checkOutput(args.srPath)
checkOutput(args.sbPath)
checkOutput(args.srOutput)
checkOutput(args.sbOutput)

for file in rootFilesList:
	fileName = file.strip(args.source)
	blindTree.cutTree(args.tree, file, args.sbPath + '/' + fileName, args.srPath + '/' + fileName)

srFileList = glob.glob("{}/*.root".format(args.srPath))
sbFileList = glob.glob("{}/*.root".format(args.sbPath))

onlyReRecoYearDict = {"run2": ["2018ReReco", "2017ReReco", "2016ReReco", "2016APVReReco"], "2016APV": ["2016APVReReco"], "2016": ["2016ReReco"], "2017": ["2017ReReco"], "2018": ["2018ReReco"]}
onlyULYearDict = {"run2": ["2018UL", "2017UL", "2016UL", "2016APVUL"], "2016APV": ["2016APVUL"], "2016": ["2016UL"], "2017": ["2017UL"], "2018": ["2018UL"]}
bothULReRecoYearDict = {"run2": ["2018ReReco", "2018UL", "2017ReReco", "2017UL", "2016ReReco", "2016UL", "2016APVReReco", "2016APVUL"], "2016APV": ["2016APVReReco", "2016APVUL"], "2016": ["2016ReReco", "2016UL"], "2017": ["2017ReReco", "2017UL"], "2018": ["2018ReReco", "2018UL"]}

print("Categorize Signal Region")
categorizeTree.categoryHistFromTree("zh", onlyReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("zjets", bothULReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("zz", bothULReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("tt", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("st", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("qcd", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	

print("Categorize Sideband Region")
categorizeTree.categoryHistFromTree("zh", onlyReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("zjets", bothULReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("zz", bothULReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("tt", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("st", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("qcd", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("data", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	