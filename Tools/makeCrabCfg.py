import json
import argparse
import os

parse = argparse.ArgumentParser()
parse.add_argument("-i", type=str, help="input json file")
parse.add_argument("-o", type=str, default="./output", help="output path, default = ./output")
parse.add_argument("-n", type=str, help="task name e.g. ZHTree")
parse.add_argument("--date", type=str, help="date (YYMMDD)")
parse.add_argument("--type", type=str, help="dataset type, input data or mc")
parse.add_argument("--pset", type=str, help="config.JobType.psetName, cfg.py e.g. ZHAnalysis_cfg.py")
parse.add_argument("--psetreco", type=str, help="config.JobType.psetName for ReReco samples, cfg.py e.g. ZHAnalysis_cfg.py")
parse.add_argument("--temp", type=str, default="crabConfig.py", help="the template of carbConfig, default = crabConfig.py")
args = parse.parse_args()

if os.path.exists(args.o): pass
else: 
    print("Create the output path {}".format(args.o))
    os.mkdir(args.o)

primary_name_list = []
datasetNameDict = {}
new_crab_cfg_list = []
new_str = ''

with open(args.temp, 'r') as cfg_template:
    file_content = cfg_template.readlines()
'''
for i in file_content:
    if 'config.JobType.psetName' in i:
        file_content_index = file_content.index(i)
        file_content[file_content_index] = "config.JobType.psetName = '{}'\n".format(args.pset)
'''
with open(args.i, 'r') as mcinfo:
    sample_list = json.load(mcinfo)

for sample in sample_list:
    for key, value in sample.items():
        if key == "primary_name":
            datasetNameDict[value] = sample["dasname"]
            break

for name, dasName in datasetNameDict.items():
    if 'UL' in dasName: pset = args.pset
    else: pset = args.psetreco
    for i in file_content:
        new_str = i
        if 'config.JobType.psetName' in i:
            new_str = "config.JobType.psetName = '{}'\n".format(pset)
        if "config.General.requestName" in i:
            new_str = "config.General.requestName = '{}_{}_{}'\n".format(name, args.n, args.date)
        if "config.Data.inputDataset" in i:
            new_str = "config.Data.inputDataset = '{}'\n".format(dasName)
        if "config.Data.outputDatasetTag" in i:
            if args.type == 'data':
                new_str = "config.Data.outputDatasetTag = '{}_{}_{}'\nconfig.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'\n".format(name, args.n, args.date)
            elif args.type == 'mc':
                new_str = "config.Data.outputDatasetTag = '{}_{}_{}'\n".format(name, args.n, args.date)
        new_crab_cfg_list.append(new_str)
    crab_file_name = "crabConfig_{}.py".format(name)
    print("Generate {}".format(crab_file_name))
    with open(args.o + '/' + crab_file_name, 'w') as crabcfg:
        crabcfg.writelines(new_crab_cfg_list)
    new_crab_cfg_list = []
