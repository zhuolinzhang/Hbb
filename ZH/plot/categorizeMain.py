import blindTree
import categorizeTree
import argparse
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument("-srPath", default= "./sr", help="The path of signal region samples")
parser.add_argument("-srOutput", default="./SRcategorizedTree", help="The path of output hists")
parser.add_argument("-sbPath", default= "./sideband", help="The path of sideband samples")
parser.add_argument("-sbOutput", default="./SBcategorizedTree", help="The path of output hists")
parser.add_argument("-sbForHM", default="./sbHiggsMass", help="The path of sideband samples only for plotting Higgs mass")
parser.add_argument("-sbForHMOut", default="./SBcategorizedHiggsMass", help="The path of output hists for plotting Higgs mass")
parser.add_argument("-tree", default="ZHCandidates", help="The name of TTree")
parser.add_argument("-source", default="./source", help="The path of source")
parser.add_argument("-y", default="run2", help="The year of datasets")
parser.add_argument("-w", action="store_true", help="Use MuonTnP SFs")
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
checkOutput(args.sbForHM)
checkOutput(args.srOutput)
checkOutput(args.sbOutput)
checkOutput(args.sbForHMOut)

for file in rootFilesList:
	fileName = file.strip(args.source)
	blindTree.cutTree(args.tree, file, "{}/{}".format(args.sbPath, fileName), "{}/{}".format(args.sbForHM, fileName), "{}/{}".format(args.srPath, fileName))

onlyReRecoYearDict = {"run2": ["2018ReReco", "2017ReReco", "2016ReReco", "2016APVReReco"], "2016APV": ["2016APVReReco"], "2016": ["2016ReReco"], "2017": ["2017ReReco"], "2018": ["2018ReReco"]}
onlyULYearDict = {"run2": ["2018UL", "2017UL", "2016UL", "2016APVUL"], "2016APV": ["2016APVUL"], "2016": ["2016UL"], "2017": ["2017UL"], "2018": ["2018UL"]}
bothULReRecoYearDict = {"run2": ["2018ReReco", "2018UL", "2017ReReco", "2017UL", "2016ReReco", "2016UL", "2016APVReReco", "2016APVUL"], "2016APV": ["2016APVReReco", "2016APVUL"], "2016": ["2016ReReco", "2016UL"], "2017": ["2017ReReco", "2017UL"], "2018": ["2018ReReco", "2018UL"]}

print("Categorize Signal Region")
categorizeTree.categoryHistFromTree("zh", onlyReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput, args.w)	
categorizeTree.categoryHistFromTree("zjets", bothULReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput, args.w)	
categorizeTree.categoryHistFromTree("zz", bothULReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput, args.w)	
categorizeTree.categoryHistFromTree("tt", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput, args.w)	
categorizeTree.categoryHistFromTree("st", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput, args.w)	
categorizeTree.categoryHistFromTree("qcd", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput, args.w)	

print("Categorize Sideband Region")
categorizeTree.categoryHistFromTree("zh", onlyReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput, args.w)
categorizeTree.categoryHistFromTree("zjets", bothULReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput, args.w)	
categorizeTree.categoryHistFromTree("zz", bothULReRecoYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput, args.w)	
categorizeTree.categoryHistFromTree("tt", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput, args.w)	
categorizeTree.categoryHistFromTree("st", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput, args.w)	
categorizeTree.categoryHistFromTree("qcd", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput, args.w)	
categorizeTree.categoryHistFromTree("data", onlyULYearDict[args.y], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput, False)	

print("Categorize Sideband Region For Plot Higgs Mass")
categorizeTree.categoryHistFromTree("zh", onlyReRecoYearDict[args.y], ["mass"], args.sbForHM, args.sbForHMOut, args.w)	
categorizeTree.categoryHistFromTree("zjets", bothULReRecoYearDict[args.y], ["mass"], args.sbForHM, args.sbForHMOut, args.w)	
categorizeTree.categoryHistFromTree("zz", bothULReRecoYearDict[args.y], ["mass"], args.sbForHM, args.sbForHMOut, args.w)	
categorizeTree.categoryHistFromTree("tt", onlyULYearDict[args.y], ["mass"], args.sbForHM, args.sbForHMOut, args.w)	
categorizeTree.categoryHistFromTree("st", onlyULYearDict[args.y], ["mass"], args.sbForHM, args.sbForHMOut, args.w)	
categorizeTree.categoryHistFromTree("qcd", onlyULYearDict[args.y], ["mass"], args.sbForHM, args.sbForHMOut, args.w)	
categorizeTree.categoryHistFromTree("data", onlyULYearDict[args.y], ["mass"], args.sbForHM, args.sbForHMOut, False)	