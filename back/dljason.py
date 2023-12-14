import os
import requests
import json

# Patch_num will be updated with update_patch function ; jason_dir should fit where we stock dl json files
patch_num = "13.22.1"
current_directory = os.path.dirname(os.path.abspath(__file__))
jason_dir = os.path.join(current_directory, 'jasons')


# Function to get the patch from the version file
def update_patch():
    url_version = "https://ddragon.leagueoflegends.com/api/versions.json"
    response = requests.get(url_version)
    if response.status_code == 200:
        file_path = os.path.join(jason_dir, 'versions.json')
        with open(file_path, "wb") as file:
            file.write(response.content)
            file.close()
        print(f"New versions.json downloaded")
    else:
        print("Failed to DL versions.json")
    with open(os.path.join(jason_dir, 'versions.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
        live_patch = data[0]
        file.close()
    return live_patch


# Function to flatten my json, find it easier to get the champ name somehow
def flatten_json(json_data, prefix=''):
    flattened = {}
    for key, value in json_data.items():
        if isinstance(value, dict):
            flattened.update(flatten_json(value, prefix + key + '.'))
        else:
            flattened[prefix + key] = value
    return flattened


patch_num = update_patch()


# Getting the list of all champions from champion.json file
def champ_lst():
    url_version = f"https://ddragon.leagueoflegends.com/cdn/{patch_num}/data/en_US/champion.json"
    response = requests.get(url_version)
    if response.status_code == 200:
        file_path = os.path.join(jason_dir, 'champion.json')
        with open(file_path, "wb") as file:
            file.write(response.content)
            file.close()
        print(f"New champion.json downloaded")
    else:
        print("Failed to DL champion.json")
    with open(os.path.join(jason_dir, 'champion.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
        flattened_json = flatten_json(data)
        chp_lst = [flattened_json[key] for key in flattened_json if key.endswith('.id')]
        file.close()
    return chp_lst


# Getting the id of all champions from champion.json file
def champ_id_lst():
    with open(jason_dir + 'champion.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        flattened_json = flatten_json(data)
        id_lst = [flattened_json[key] for key in flattened_json if key.endswith('.key')]
        file.close()
    return id_lst


champions_list = champ_lst()


# Here we download all the champions json files, only need to update patch_num from time to time
def dl_champ_json():
    updates_jasons = input("Do you need to update the files ? (yes/no)")
    if updates_jasons.lower() == 'yes':
        for champ_name in champions_list:
            url_cdn = f'https://cdn.communitydragon.org/{patch_num}/champion/{champ_name}/data'
            response = requests.get(url_cdn)

            if response.status_code == 200:
                file_path = os.path.join(jason_dir, f'{champ_name}.json')
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"File downloaded successfully to {file_path}")
            else:
                print(f"Failed to download the file for {champ_name}")
        print("I updated the json files.")
    else:
        print("I did not updated the json files this time.")
    return print("Download complete !")
