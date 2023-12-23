import json
import os
import pandas as pd
from back.dljason import champions_list, patch_num

current_directory = os.path.dirname(os.path.abspath(__file__))
jason_dir = os.path.join(current_directory, 'jasons')


# Formatting function to remove trailing zeros, will bug if apply to strings
def format_numbers(val):
    return f'{val:.0f}' if val.is_integer() else f'{val:.2f}'.rstrip('0').rstrip('.')


# Function to generate the full dataframe Q1 to R6 for all champs (champ_lst for columns)
def champ_dataframe():
    spell_lst = ['q', 'w', 'e', 'r']
    rank_lst = [1, 2, 3, 4, 5, 6]
    sr_lst = [f'{letter}{number}' for letter in spell_lst for number in rank_lst]  # The list from Q1 to R6
    sr_lst.insert(0, "Name")  # Same list + Name at the start
    df = pd.DataFrame(columns=sr_lst)

    for champ_name in champions_list:
        with open(os.path.join(jason_dir, f'{champ_name}.json'), 'r', encoding='utf-8') as user_file:
            parsed_json = json.load(user_file)

        cd_lst = []
        for spell in parsed_json.get("spells", []):
            if spell.get("spellKey") in spell_lst:
                ammo_value = spell.get("ammo", {}).get("ammoRechargeTime", [])
                cooldown_values = spell.get("cooldownCoefficients", [])

                for ammo, cooldown in zip(ammo_value, cooldown_values):
                    if cooldown <= ammo:
                        cd_lst.append(ammo)

                    else:
                        cd_lst.append(cooldown)
        cd_lst.insert(0, f'{champ_name}')

        sr_and_cd = dict(zip(sr_lst, cd_lst))
        df.loc[len(df)] = sr_and_cd

    # Inserting the icons columns ranks : 0, 1, 7, 14, 21
    df.insert(loc=0, column='ci', value=None)
    df.insert(loc=2, column='qi', value=None)
    df.insert(loc=9, column='wi', value=None)
    df.insert(loc=16, column='ei', value=None)
    df.insert(loc=23, column='ri', value=None)

    # Function to generate image URL based on 'Name'
    def generate_name_img(name):
        return f"<img src='https://cdn.communitydragon.org/{patch_num}/champion/{name}/square.png' " \
               f"class='cdn-img' loading='lazy'>"

    def generate_q_spell_img(name):
        return f"<img src='https://cdn.communitydragon.org/{patch_num}/champion/{name}/ability-icon/q' " \
               f"class='cdn-img' loading='lazy'>"

    def generate_w_spell_img(name):
        return f"<img src='https://cdn.communitydragon.org/{patch_num}/champion/{name}/ability-icon/w' " \
               f"class='cdn-img' loading='lazy'>"

    def generate_e_spell_img(name):
        return f"<img src='https://cdn.communitydragon.org/{patch_num}/champion/{name}/ability-icon/e' " \
               f"class='cdn-img' loading='lazy'>"

    def generate_r_spell_img(name):
        return f"<img src='https://cdn.communitydragon.org/{patch_num}/champion/{name}/ability-icon/r' " \
               f"class='cdn-img' loading='lazy'>"

    # Apply the function to populate the specific columns
    df['ci'] = df['Name'].apply(generate_name_img)
    df['qi'] = df['Name'].apply(generate_q_spell_img)
    df['wi'] = df['Name'].apply(generate_w_spell_img)
    df['ei'] = df['Name'].apply(generate_e_spell_img)
    df['ri'] = df['Name'].apply(generate_r_spell_img)

    # Should add the morph exceptions here : Elise Spider, Jayce cannon, Nidalee cat

    header_lst = df.columns.tolist()
    # ['ci', 'Name', 'qi', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'wi', 'w1', 'w2', 'w3', 'w4', 'w5', 'w6',
    #                'ei', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'ri', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6']

    # elise spider form building
    elise_path_ico = "https://raw.communitydragon.org/latest/game/assets/characters/elise/hud/elise_circle.png"
    elise_path_s = "https://raw.communitydragon.org/pbe/game/assets/characters/elise/hud/icons2d/elise"
    elise_spider_spells = [f"<img src='{elise_path_ico}' width='40'>",
                           'Elise Spider',
                           f"<img src='{elise_path_s}spiderq.png' class='cdn-img' loading='lazy'>",
                           6, 6, 6, 6, 6, 6,
                           f"<img src='{elise_path_s}spiderw.png' class='cdn-img' loading='lazy'>",
                           10, 10, 10, 10, 10, 10,
                           f"<img src='{elise_path_s}spidere.png' class='cdn-img' loading='lazy'>",
                           22, 21, 20, 19, 18, 18,
                           f"<img src='{elise_path_s}r.png' class='cdn-img' loading='lazy'",
                           4, 4, 4, 4, 4, 4]
    elise_sf = dict(zip(header_lst, elise_spider_spells))

    # jayce cannon form building
    jayce_path_ico = "https://raw.communitydragon.org/latest/game/assets/characters/jayce/hud/jayce_circle.png"
    jayce_path_s = "https://raw.communitydragon.org/latest/game/assets/characters/jayce/hud/icons2d/jayce"
    jayce_c_s = [f"<img src='{jayce_path_ico}' width='40'>",
                 'Jayce Cannon',
                 f"<img src='{jayce_path_s}q_ranged.jaycenewicons.png' class='cdn-img' loading='lazy'>",
                 8, 8, 8, 8, 8, 8,
                 f"<img src='{jayce_path_s}w_ranged.jaycenewicons.png' class='cdn-img' loading='lazy'>",
                 13, 11.4, 9.8, 8.2, 6.6, 5,
                 f"<img src='{jayce_path_s}e_ranged.jaycenewicons.png' class='cdn-img' loading='lazy'>",
                 16, 16, 16, 16, 16, 16,
                 f"<img src='{jayce_path_s}r_melee.jaycenewicons.png' class='cdn-img' loading='lazy'>",
                 6, 6, 6, 6, 6, 6]
    jayce_sf = dict(zip(header_lst, jayce_c_s))

    # nidalee cougar form building
    nidalee_path_ico = "https://raw.communitydragon.org/latest/game/assets/characters/nidalee/hud/nidalee_circle.png"
    nidalee_path_s = "https://raw.communitydragon.org/latest/game/assets/characters/nidalee/hud/icons2d/nidalee_"
    nidalee_c_s = [f"<img src='{nidalee_path_ico}' class='cdn-img'>",
                   'Nidalee Cougar',
                   f"<img src='{nidalee_path_s}q2.png' class='cdn-img' loading='lazy'>",
                   6, 6, 6, 6, 6, 6,
                   f"<img src='{nidalee_path_s}w2.png' class='cdn-img' loading='lazy'>",
                   6, 6, 6, 6, 6, 6,
                   f"<img src='{nidalee_path_s}e2.png' class='cdn-img' loading='lazy'>",
                   6, 6, 6, 6, 6, 6,
                   f"<img src='{nidalee_path_s}r2.png' class='cdn-img' loading='lazy'>",
                   3, 3, 3, 3, 3, 3]

    nidalee_sf = dict(zip(header_lst, nidalee_c_s))

    # add the new rows to the data frame
    """elise_idx = df[df['Name'] == 'Elise'].index[0] + 1
    df.loc[elise_idx] = elise_sf"""
    df.loc[len(df)] = elise_sf

    df.loc[len(df)] = jayce_sf

    df.loc[len(df)] = nidalee_sf

    # here we add the specific spells exceptions that are lost in json
    col_q = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
    col_w = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6']
    col_e = ['e1', 'e2', 'e3', 'e4', 'e5', 'e6']
    col_r = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6']  # maybe in the future kekw

    aurel_idx = df[df['Name'] == 'AurelionSol'].index.tolist()[0]
    aurel_w = [22, 20.5, 19, 17.5, 16, 16]
    df.loc[aurel_idx, col_w] = aurel_w

    belveth_idx = df[df['Name'] == 'Belveth'].index.tolist()[0]
    belveth_q = [16, 15, 14, 13, 12, 12]
    df.loc[belveth_idx, col_q] = belveth_q

    kalista_idx = df[df['Name'] == 'Kalista'].index.tolist()[0]
    kalista_e = [10, 9.5, 9, 8.5, 8, 8]
    df.loc[kalista_idx, col_e] = kalista_e

    veigar_idx = df[df['Name'] == 'Veigar'].index.tolist()[0]
    veigar_w = [8, 8, 8, 8, 8, 8]
    df.loc[veigar_idx, col_w] = veigar_w

    yuumi_idx = df[df['Name'] == 'Yuumi'].index.tolist()[0]
    yuumi_w = [10, 10, 5, 5, 0, 0]
    df.loc[yuumi_idx, col_w] = yuumi_w

    zeri_idx = df[df['Name'] == 'Zeri'].index.tolist()[0]
    zeri_q = [1, 1, 1, 1, 1, 1]
    df.loc[zeri_idx, col_q] = zeri_q

    # Monkey King to wukong
    monkey_idx = df[df['Name'] == 'MonkeyKing'].index.tolist()[0]
    df.loc[monkey_idx, 'Name'] = 'Wukong'

    # Sorting & cleaning the DF a bit
    nbs_columns = [3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 21, 22, 23]
    png_columns = [0, 2, 8, 14, 20]

    df.sort_values(by='Name', inplace=True)
    df.columns = df.columns.str.upper()
    columns_to_drop = ["Q6", "W6", "E6", "R4", "R5", "R6"]
    df = df.drop(columns=columns_to_drop, axis=1)
    df = df.round(2)

    # Apply the formatting function to the DataFrame avoiding URL & Name cells
    df.iloc[:, nbs_columns] = df.iloc[:, nbs_columns].map(format_numbers)

    user_file.close()
    return df
