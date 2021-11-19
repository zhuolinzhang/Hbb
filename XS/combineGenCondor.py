import os
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="datacard path")
args = parser.parse_args()

os.chdir(args.i)
for cardName in glob.glob("*.txt"):
    mass = float(cardName[cardName.find("mH") + 2: -4])
    print("Generate {}".format(cardName))
    os.system("combineTool.py -M AsymptoticLimits -d {0} -n .test.pt{1} -m 125 --noFitAsimov --job-mode condor --task-name pt_{1} --sub-opts='+JobFlavour=\"tomorrow\"'".format(cardName, mass))
