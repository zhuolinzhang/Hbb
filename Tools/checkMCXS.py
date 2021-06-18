import os

mcFileList = []
with open("./MCXSList.txt") as f:
    for i in f:
        mcFileList.append(i.rstrip())

for i in mcFileList:
    os.system('cmsRun ana.py inputFiles="file:root://cmsxrootd.fnal.gov/{}" maxEvents=-1'.format(i))