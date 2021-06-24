import os
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="datacard path")
args = parser.parse_args()

os.chdir(args.i)
for file in glob.glob(".txt"):
	mass = float(file[file.find("mH") + 2, -4])
	print("Now calculate {}".format(mass))
	os.system("combine -M AsymptoticLimits {} -m {} -n test --run blind".format(file, mass))