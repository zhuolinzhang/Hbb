import json
import os
import re

primary_name_list = []
dataset_list = []
dataset_dict = {}
new_crab_cfg_list = []
new_str = ''
task_name = input("Please input the task name: ")
date = input("Please input the date of submitting (YYMMDD): ")
psetName = input("Please input the config.JobType.psetName: ")

with open("crabConfig.py", 'r') as cfg_template:
    file_content = cfg_template.readlines()

for i in file_content:
    if re.search('config.JobType.psetName', i):
        file_content_index = file_content.index(i)
        file_content[file_content_index] = "config.JobType.psetName = '{}'\n".format(psetName)

with open('DataInfo.json', 'r') as mcinfo:
    sample_list = json.load(mcinfo)

for sample in sample_list:
    for key, value in sample.items():
        if key == "primary_name":
            primary_name_list.append(value)
            break

for name in primary_name_list:
    for i in dataset_list:
        if re.search(name, i):
            dataset_dict[name] = i

for name in primary_name_list:
    for i in file_content:
        new_str = i
        if re.search("config.General.requestName", i):
            new_str = "config.General.requestName = '{}_{}_{}'\n".format(name, task_name, date)
        if re.search("config.Data.inputDataset", i):
            for sample in sample_list:
                if sample["primary_name"] == name:
                    dataset_name = sample["dasname"] 
            new_str = "config.Data.inputDataset = '{}'\n".format(dataset_name)
        if re.search("config.Data.outputDatasetTag", i):
            new_str = "config.Data.outputDatasetTag = '{}_{}_{}'\n".format(name, task_name, date)
        new_crab_cfg_list.append(new_str)
    
    crab_file_name = "crabConfig_{}.py".format(name)
    with open(crab_file_name, 'w') as crabcfg:
        crabcfg.writelines(new_crab_cfg_list)
    new_crab_cfg_list = []
