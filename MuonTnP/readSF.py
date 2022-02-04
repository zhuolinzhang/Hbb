import glob
import os
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-i", default="./input", help="The folder which you want to scan")
parser.add_argument("-o", default=".", help="The folder which you want to save root files")
args = parser.parse_args()

if os.path.exists(args.o): pass
else: os.mkdir(args.o)

rootFileList = glob.glob("{}/*.root".format(args.i))
for file in rootFileList:
	fileName = file.split('/')[-1]
	if "DoubleMuon" in file: 
		print("{} is data! Copy the file to the output path".format(fileName))
		shutil.copy(file, "{}/{}".format(args.o, fileName))
	print("Calculate Muon TnP SFs in {}".format(fileName))
	os.system("root -q -l -b 'readSF.C(\"{}\", \"{}/{}\",\"/Users/zhangzhuolin/Hbb/MuonTnP/MuonPOGSF\")'".format(file, args.o, fileName))