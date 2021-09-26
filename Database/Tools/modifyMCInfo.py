import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="The path of json file")
args = parser.parse_args()

# load json database
origin_database = []
with open(args.i, "r") as database_json:
    origin_database = json.load(database_json)

# modify items or add items in the json file
option = input("Please input the option to add or modify items in the json database (a/m): ")
# add items
if option == 'a':
    add_item = input("Please input the item name which you want to add for each dataset: ")
    for dataset_dict in origin_database:
        print("You are modifying", dataset_dict["primary_name"])
        add_content = input("Please input the content which you want to add (enter q to quit): ")
        if add_content == 'q':
            break
        dataset_dict[add_item] = add_content
    with open("MCInfo.json", 'w') as new_data_json:
        json.dump(origin_database, new_data_json, indent=4)
# modify items
elif option == 'm':
    modify_dataset = input("Pleas input the primary name of the dataset which you want to modify (enter every will modify the item in every dataset): ")
    if modify_dataset != "every":
        modify_item = input("Please input the item you want to modify: ")
        while modify_dataset != 'q':
            modify_content = input("Please input the new item value: ")
            for dataset_dict in origin_database:
                if dataset_dict["primary_name"] == modify_dataset:
                    print("Success!")
                    dataset_dict[modify_item] = modify_content
            modify_dataset = input("Input another primary name of dataset which you want to modify or enter q to quit: ")
        with open("MCInfo.json", 'w') as new_data_json:
            json.dump(origin_database, new_data_json, indent=4)
    elif modify_dataset == "every":
        modify_item = input("Please input the item you want to modify: ")
        for dataset_dict in origin_database:
            print("You are modifying", dataset_dict["primary_name"])
            modify_content = input("Please input the new item value (enter q to quit): ")
            if modify_content == 'q':
                break
            dataset_dict[modify_item] = modify_content
        with open("MCInfo.json", 'w') as new_data_json:
            json.dump(origin_database, new_data_json, indent=4)
else:
    print("You input a wrong option, the script will quit.")
