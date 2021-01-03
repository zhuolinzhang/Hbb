# This script will check the number of events for each dataset and correct it. Then, it will calculate the right normalization factor
# This script MUST be run on the LXPLUS!!!

import os
import json

database_list = []
with open("MCInfo.json", 'r') as database_json:
    database_list = json.load(database_json)

lumi_2018data = 59.74
event = 1

for dataset_dict in database_list:
    for key, value in dataset_dict.items():
        if key == "dasname":
            os.system('dasgoclient -query="dataset=%s" -json > datainfo.json' % value)
            with open("datainfo.json", 'r') as das_json:
                das_info = json.load(das_json)
            for dict_ele in das_info:
                for key, value in dict_ele["das"].items():
                    if key == "services":
                        for i in value:
                            if i == "dbs3:filesummaries":
                                for j in dict_ele["dataset"]:
                                    for key, value in j.items():
                                        if key == "nevents":
                                            event = value
                                    break
        if dataset_dict["nevents"] == event:
            continue
        else:
            dataset_dict["nevents"] = event
            dataset_dict["factor_2018"] = lumi_2018data / ((event / dataset_dict["xsection"]) / 1000)

with open("MCInfo.json", 'w') as new_data_json:
    json.dump(database_list, new_data_json, indent=4)