import os
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="datacard path")
args = parser.parse_args()

os.chdir(args.i)
for i in glob.glob("*.txt"):
    #mass = float(i[i.find("mH") + 2: -4])
    print("Now calculate {}".format(i))
    os.system("combine -M AsymptoticLimits {} -n test -m 125 --run blind".format(i))
