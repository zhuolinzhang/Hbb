import ROOT
import os

def open_file(file_path):
    # Load root files in a folder
    file_list = os.listdir(file_path)
    root_file_list = []
    # Remove annoying .DS_Store (it is not needed on Linux)
    for i in file_list:
        if i == '.DS_Store':
            file_list.remove('.DS_Store')
    for file_name in file_list:
        file_name = file_path + '/' + file_name
        root_file_list.append(ROOT.TFile(file_name))
    return root_file_list

def get_primary_name(list_index, file_path = './Samples'):
    # Get the file name without suffix to help analysis
    file_list = os.listdir(file_path)
    file_name = file_list[list_index]
    primary_name = file_name.rstrip('.root')
    return primary_name