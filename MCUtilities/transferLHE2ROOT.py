import argparse
import os
import xml.etree.ElementTree as ET
import shutil
import gzip

def extractLHE(path):
	newLHEPath = path.rstrip(".lhe.gz") + ".lhe"
	with gzip.open(path, 'rb') as fIn:
		with open(newLHEPath, 'wb') as fOut: 
			shutil.copyfileobj(fIn, fOut)
	xmlTree = ET.parse(newLHEPath)
	xmlRoot = xmlTree.getroot()
	xs = 0.
	for num in xmlRoot.iter('init'):
		xs = float(num.text.split()[-4])
	return xs

parser = argparse.ArgumentParser()
parser.add_argument("-n", help="The output folder name")
parser.add_argument("-r", help="The run number")
args = parser.parse_args()

# Find LHE file or ROOT exported from LHE
eventPath = "./{}/Events".format(args.n)
runList = os.listdir(eventPath)
outputPath = ''
xs = 0.
if len(runList) < 1: raise SystemExit("Your Events is empty! Please check the result!")
elif len(runList) == 1: 
	outputPath = eventPath + "/run_01"
elif len(runList) > 1:
	if not args.r: raise SystemExit("You must input a run number!")
	outputPath = eventPath + "/run_{}".format(args.r)
outputList = os.listdir(outputPath)
newLHEPath = outputPath + "/" + "{}.lhe.gz".format(args.n)
findLHEFlag = False
findExROOTFlag = False
for file in outputList:
	if "events.root" in file:
		shutil.copy(outputPath + "/" + file, "../ExRootAnalysis/{}.root".format(args.n))
		findExROOTFlag = True
		continue
	if ".lhe.gz" in file:
		if args.n in file: continue
		shutil.copy(outputPath + "/" + file, newLHEPath)
		findLHEFlag = True
		break
if not(findLHEFlag): raise SystemExit("The script can't find .lhe.gz in your run folder! Please check the result!")
xs = extractLHE(outputPath + "/" + "{}.lhe.gz".format(args.n))
if not(findExROOTFlag):
	shutil.copy(newLHEPath, "../ExRootAnalysis")
	os.system("../ExRootAnalysis/ExRootLHEFConverter ../ExRootAnalysis/{0}.lhe ../ExRootAnalysis/{0}.root".format(args.n))
runROOTCommand = "root -q -b -l '../ExRootAnalysis/plotLHEXS.C(\"../ExRootAnalysis/{}.root\", {}, \"../ExRootAnalysis/libExRootAnalysis.so\")'".format(args.n, xs)
os.system(runROOTCommand)