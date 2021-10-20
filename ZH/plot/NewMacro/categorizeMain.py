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
args = parser.parse_args()

def checkOutput(path: str) -> None:
	if os.path.exists(path): pass
	else: os.mkdir(path)

rootFilesList = glob.glob("{}/*.root".format(args.source))
checkOutput(args.srPath)
checkOutput(args.sbPath)
checkOutput(args.srOutput)
checkOutput(args.sbOutput)
'''
for file in rootFilesList:
	fileName = file.strip(args.source)
	blindTree.cutTree(args.tree, file, args.sbPath + '/' + fileName, args.srPath + '/' + fileName)
'''
srFileList = glob.glob("{}/*.root".format(args.srPath))
sbFileList = glob.glob("{}/*.root".format(args.sbPath))

categorizeTree.categoryHistFromTree("zh", ["2018ReReco"], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("zjets", ["2018ReReco", "2018UL"], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("zz", ["2018ReReco", "2018UL"], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("tt", ["2018UL"], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("st", ["2018UL"], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	
categorizeTree.categoryHistFromTree("qcd", ["2018UL"], ["mass", "pt", "eta", "phi"], args.srPath, args.srOutput)	

categorizeTree.categoryHistFromTree("zh", ["2018ReReco"], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("zjets", ["2018ReReco", "2018UL"], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("zz", ["2018ReReco", "2018UL"], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("tt", ["2018UL"], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("st", ["2018UL"], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("qcd", ["2018UL"], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	
categorizeTree.categoryHistFromTree("data", ["2018UL"], ["mass", "pt", "eta", "phi"], args.sbPath, args.sbOutput)	