import os
import re

dib = []
dy_jets_to_ll = []
dy_jets_to_ll_tuneCP5 = []
dy_jets_to_ll_tuneCP5_m50 = []
dy_bjets_to_ll_tuneCP5_m50_zpt = []
dy_jets_bgf = []
st = []
qcd = []

menu_new = []
crab_line = []
crab_line_new = []

with open("samplesInHbbAnalysis.md","r") as menu:
    for line in menu:
        menu_old = menu.readlines()

# delete \n
for i in menu_old:
    menu_new.append(i[:-1])

while '' in menu_new:
    menu_new.remove('')

for i in menu_new:
    if re.search('#',i):
        continue
    if re.search('nevents',i):
        continue
    # diboson bkg
    if re.search('`/ZZ_TuneCP5_13TeV',i):
        dib.append(i[1:-1])
        continue
    if re.search('`/ZZTo2L2Q',i):
        dib.append(i[1:-1])
        continue
    # z to ll bkg
    if re.search('/DYJetsToLL_M-4to50_HT',i):
        dy_jets_to_ll.append(i[1:-1])
        continue
    if re.search('`/DYJetsToLL_M-50_TuneCP5',i):
        dy_jets_to_ll_tuneCP5.append(i[1:-1])
        continue
    if re.search('`/DYJetsToLL_M-50_HT',i):
        dy_jets_to_ll_tuneCP5_m50.append(i[1:-1])
        continue
    if re.search('`/DYBJetsToLL_M-50_Zpt',i):
        dy_bjets_to_ll_tuneCP5_m50_zpt.append(i[1:-1])
        continue
    if re.search('`/DYJetsToLL_BGenFilter',i):
        dy_jets_bgf.append(i[1:-1])
        continue
    # tt, QCD
    if re.search('`/ST',i):
        st.append(i[1:-1])
        continue
    if re.search('`/QCD',i):
        qcd.append(i[1:-1])
        continue

path = "./crab_cfg"

for file in os.listdir(path):
    file_name = path + '/' + file
    crab_cfg_file_old = open(file_name,"r")
    crab_line = crab_cfg_file_old.readlines()
    for i in crab_line:
        if "config.JobType.psetName = 'MuonExercise2.py'\n" in i:
            crab_line[8] = "config.JobType.psetName = 'ZpeakBkg_cfg.py'\n"
        
    if "Dib_1" in file_name:
        crab_line[3] = "config.General.requestName = 'diboson_bkg_ZZ_TuneCP5'\n"
        crab_line[11] = "config.Data.inputDataset = '" + dib[0] + "'\n"
        crab_line[14] = "config.Data.outputDatasetTag = 'diboson_bkg_ZZ_TuneCP5'\n"

    if "Dib_2" in file_name:
        crab_line[3] = "config.General.requestName = 'diboson_bkg_ZZTo2L2Q'\n"
        crab_line[11] = "config.Data.inputDataset = '" + dib[1] + "'\n"
        crab_line[14] = "config.Data.outputDatasetTag = 'diboson_bkg_ZZTo2L2Q'\n"

    if "DYJetsToLL_" in file_name:
        crab_line[3] = "config.General.requestName = '" + file_name[-15:-3] + "'\n"
        crab_line[11] = "config.Data.inputDataset = '" + dy_jets_to_ll[int(file_name[-4]) - 1] + "'\n"
        crab_line[14] = "config.Data.outputDatasetTag = '" + file_name[-15:-3] + "'\n"
    
    if "DYJetsToLLTuneCP5.py" in file_name:
        crab_line[3] = "config.General.requestName = '" + file_name[-20:-3] + "'\n"
        crab_line[11] = "config.Data.inputDataset = '" + dy_jets_to_ll_tuneCP5[0] + "'\n"
        crab_line[14] = "config.Data.outputDatasetTag = '" + file_name[-20:-3] + "'\n"
    
    if "DYJetsToLLTuneCP5_M-50_" in file_name:
        crab_line[3] = "config.General.requestName = '" + file_name[-27:-3] + "'\n"
        crab_line[11] = "config.Data.inputDataset = '" + dy_jets_to_ll_tuneCP5_m50[int(file_name[-4]) - 1] + "'\n" 
        crab_line[14] = "config.Data.outputDatasetTag = '" + file_name[-27:-3] + "'\n"
    
    if "DYBJetsToLLTuneCP5" in file_name:
        crab_line[3] = "config.General.requestName = '" + file_name[-32:-3] + "'\n"
        crab_line[11] = "config.Data.inputDataset = '" + dy_bjets_to_ll_tuneCP5_m50_zpt[int(file_name[-4]) - 1] + "'\n"
        crab_line[14] = "config.Data.outputDatasetTag = '" + file_name[-32:-3] + "'\n"
    
    if "DYJetsToLLTuneCP5_M-50BGF" in file_name:
        crab_line[3] = "config.General.requestName = '" + file_name[-34:-3] + "'\n"
        crab_line[11] = "config.Data.inputDataset = '" + dy_jets_bgf[int(file_name[-4]) - 1] + "'\n" 
        crab_line[14] = "config.Data.outputDatasetTag = '" + file_name[-34:-3] + "'\n"
    
    if "_ST" in file_name:
        crab_line[3] = "config.General.requestName = 'single_t_" + file_name[-7:-3] + "'\n"
        crab_line[11] = "config.Data.inputDataset = '" + st[int(file_name[-4]) - 1] + "'\n"
        crab_line[14] = "config.Data.outputDatasetTag = 'single_t_" + file_name[-7:-3] + "'\n"
    if "_QCD_" in file_name:
        crab_line[3] = "config.General.requestName = 'QCD_Bkg_" + file_name[-4:-3] + "'\n"
        crab_line[11] = "config.Data.inputDataset = '" + qcd[int(file_name[-4]) - 1] + "'\n"
        crab_line[14] = "config.Data.outputDatasetTag = 'QCD_Bkg_" + file_name[-4:-3] + "'\n"
    
    #print(crab_line)
    crab_cfg_file_old.close()

    crab_cfg_file_new = open(file_name,"w")

    for i in crab_line:
        crab_cfg_file_new.write(i)
    
    crab_cfg_file_new.close()
    
    
