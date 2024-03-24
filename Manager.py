import os
import shutil
import random
import json
import copy
import glob
import xml.etree.cElementTree as ET
from pyprc import *
from xml.dom import minidom

#hash.load_labels("ParamLabels.csv")

def init():
    global use_event_data
    use_event_data = os.path.isdir("Data\\Event")
    global spirit_list
    spirit_list = []
    global summonable
    summonable = []
    global food_type
    food_type = [
        0x1c4da84251,
        0x1cd4a113eb,
        0x1ca3a6237d,
        0x1c3dc2b6de,
        0x1c4ac58648,
        0x1cd3ccd7f2,
        0x1ca4cbe764,
        0x1c3474faf5,
        0x1c4373ca63,
        0x1c23b44386,
        0x1c54b37310,
        0x1ccdba22aa,
        0x1cbabd123c,
        0x1c24d9879f,
        0x1c53deb709,
        0x1ccad7e6b3,
        0x1cbdd0d625,
        0x1c2d6fcbb4,
        0x1c5a68fb22,
        0x1c08991045,
        0x1c7f9e20d3,
        0x1ce6977169,
        0x1c919041ff,
        0x1c0ff4d45c,
        0x1c78f3e4ca
    ]
    global reward_type
    reward_type = [
      "sp_500",
      "sp_1000",
      "sp_2000",
      "sp_3000",
      "sp_5000",
      "skill_5",
      "skill_10",
      "skill_25",
      "skill_50",
      "energy_s_1",
      "energy_s_2",
      "energy_s_3",
      "energy_s_5",
      "energy_s_10",
      "energy_m_1",
      "energy_m_2",
      "energy_m_3",
      "energy_m_5",
      "energy_l_1",
      "energy_l_2",
      "energy_l_3"
    ]
    #Rank stuff
    global rank_to_intensity
    rank_to_intensity = {
        hash("normal"): 1250,
        hash("hope")  : 1650,
        hash("ace")   : 3750,
        hash("legend"): 6250
    }
    global rank_to_star
    rank_to_star = {
        hash("normal"): 1,
        hash("hope")  : 2,
        hash("ace")   : 3,
        hash("legend"): 4
    }
    global rank_to_star_invert
    rank_to_star_invert = {value: key for key, value in rank_to_star.items()}
    #Boss chara ID to its map spirit ID, extra item and progress
    global boss_to_properties
    boss_to_properties = {
        hash("ui_chara_lioleus")  : (hash("rathian")           ,hash("")                , 1),
        hash("ui_chara_koopag")   : (hash("bowser")            ,hash("spirit_koopag")   , 1),
        hash("ui_chara_galleom")  : (hash("galleom")           ,hash("")                , 1),
        hash("ui_chara_ganonboss"): (hash("ganon_ocarina")     ,hash("")                , 2),
        hash("ui_chara_marx")     : (hash("marx")              ,hash("")                , 2),
        hash("ui_chara_dracula")  : (hash("vampire")           ,hash("spirit_dracula02"), 2)
    }
    global boss_to_properties_invert
    boss_to_properties_invert = {value[0]: key for key, value in boss_to_properties.items()}
    global spirit_to_boss
    spirit_to_boss = {
        hash("rathian")          : (hash("ui_chara_lioleus")  ),
        hash("giga_bawser")      : (hash("ui_chara_koopag")   ),
        hash("galleom")          : (hash("ui_chara_galleom")  ),
        hash("ganon_ocarina")    : (hash("ui_chara_ganonboss")),
        hash("marx")             : (hash("ui_chara_marx")     ),
        hash("marx_soul")        : (hash("ui_chara_marx")     ),
        hash("vampire")          : (hash("ui_chara_dracula")  ),
        hash("vampire_seondform"): (hash("ui_chara_dracula")  )
    }
    global boss_list
    boss_list = [
        ["giga_bawser"],
        ["galleom"],
        ["rathian"],
        ["marx"],
        ["ganon_ocarina"],
        ["vampire_seondform"],
        ["master_hand"],
        ["master_hand_final_weak",   "master_hand_final_weak_light",   "master_hand_final_weak_dark"],
        ["master_hand_final_strong", "master_hand_final_strong_light", "master_hand_final_strong_dark"],
        ["crazy_hand_a"],
        ["crazy_hand"],
        ["crazy_hand_c"],
        ["crazy_hand_final_weak",   "crazy_hand_final_weak_light",   "crazy_hand_final_weak_dark"],
        ["crazy_hand_final_strong", "crazy_hand_final_strong_light", "crazy_hand_final_strong_dark"],
        ["kiila", "kiila_1st"],
        ["kiila_twilight"],
        ["darz",  "darz_1st"],
        ["darz_twilight"],
        ["final_stage3"]
    ]
    #Master spirit ID to its subtype, activity index, activity subtype and element
    global master_to_properties
    master_to_properties = {
        hash("honey_queen")      : (hash(0x2a59b39d70), [797]         , hash(0x2aea045355), "light"),
        hash("toadett")          : (hash(0x2398f9aaa9), [793]         , hash(0x231af91025), "light"),
        hash("funky_kong")       : (hash(0x1f2b9d45c7), []            , hash(0x1f8bc1e12b), "light"),
        hash("darunia")          : (hash(0x26c5417601), [798]         , hash(0x263344d255), "light"),
        hash("beedle")           : (hash(0x1b98f4e4f7), [791]         , hash(0x1b9a1ebbce), "light"),
        hash("linebeck")         : (hash(0x2422f84412), [802]         , hash(0x24c6748ba3), "light"),
        hash("kraid")            : (hash(0x24242e1893), [222]         , hash(0x24c0a2d722),  "dark"),
        hash("peppy_hare")       : (hash(0x29c1f75be9), [804]         , hash(0x2910435011), "light"),
        hash("dr_stewart")       : (hash(0x290368eb66), [198]         , hash(0x29d2dce09e),  "dark"),
        hash("anna")             : (hash(0x19f5e68478), [790]         , hash(0x19317695e9), "light"),
        hash("ryoma")            : (hash(0x24804776e0), [799]         , hash(0x2464cbb951), "light"),
        hash("dyntos")           : (hash(0x255bc35997), [803]         , hash(0x25e7415642), "light"),
        hash("kat_and_ana")      : (hash(0x2a7ba17117), [805]         , hash(0x2ac816bf32), "light"),
        hash("captain_charlie")  : (hash(0x2bb5b7161f), [810]         , hash(0x2bfe007596), "light"),
        hash("timmy_and_tommy")  : (hash(0x24837d8277), [789]         , hash(0x2467f14dc6), "light"),
        hash("copper_and_booker"): (hash(0x30cc2908d3), [792]         , hash(0x308ad0fc86), "light"),
        hash("wii_balance_board"): (hash(0x305f1e1814), [796]         , hash(0x3019e7ec41), "light"),
        hash("doc_louis")        : (hash(0x287fa826ba), [795]         , hash(0x2870c42f1e), "light"),
        hash("riki")             : (hash(0x23525cf9bf), [801]         , hash(0x23d05c4333), "light"),
        hash("capn_cuttlefish")  : (hash(0x2e4a15a72e), [794]         , hash(0x2ebf249921), "light"),
        hash("sheldon")          : (hash(0x1c173625f0), [806]         , hash(0x1c483147a7), "light"),
        hash("slowpoke")         : (hash(0x27049da4f9), [800]         , hash(0x27686d34b0), "light"),
        hash("gravity_man")      : (hash(0x2aaaa363eb), [199]         , hash(0x2a1914adce),  "dark"),
        hash("zangief")          : (hash(0x269a3eb82f), [17, 148, 254], hash(0x266c3b1c7b), "light")
    }
    global master_to_properties_invert
    master_to_properties_invert = {value[0]: key for key, value in master_to_properties.items()}
    global all_replacement
    all_replacement = {}
    global all_replacement_invert
    all_replacement_invert = {}
    global spirit_to_index
    spirit_to_index = {}
    global spirit_to_rank
    spirit_to_rank = {}
    global spirit_to_power
    spirit_to_power = {}
    global spirit_to_type
    spirit_to_type = {}
    global spirit_to_color
    spirit_to_color = {}
    global spirit_override
    spirit_override = {}
    global spirit_logic
    spirit_logic = {
        "bomberman": {
            "spirit": [
                "cammy",
                "diggernaut",
                "eggplant_wizard",
                "zebesian",
                "medeus",
                "squawks",
                "daruk",
                "james_mccloud",
                "volcanion",
                "metroid",
                "prince_peasley"
            ],
            "area": "none",
            "lock": "none"
        },
        "megaman_exe": {
            "spirit": [
                "sigma"
            ],
            "area": "base",
            "lock": "none"
        },
        "reese_and_cyrus": {
            "spirit": [
                "yellow_wollywog",
                "kid",
                "the_boss",
                "pak_e_derm",
                "viruses",
                "camilla"
            ],
            "area": "none",
            "lock": "none"
        },
        "ho_oh": {
            "spirit": [],
            "area": "none",
            "lock": "none"
        },
        "viridi": {
            "spirit": [
                "centurion",
                "odyssey",
                "pegasus_sisters",
                "super_star",
                "revali",
                "chao",
                "tiki",
                "mallow",
                "spirit_who_loves_surprises",
                "hewdraw"
            ],
            "area": "star",
            "lock": "bomberman"
        },
        "kappn": {
            "spirit": [
                "balloon_fish",
                "mermaid",
                "star_rod"
            ],
            "area": "world_tour",
            "lock": "none"
        },
        "pico": {
            "spirit": [
                "nico_fire",
                "mach_rider",
                "motocrosser",
                "gyrowing",
                "jack_levin",
                "mighty_gazelle"
            ],
            "area": "none",
            "lock": "none"
        },
        "kappn_ww": {
            "spirit": [],
            "area": "none",
            "lock": "none"
        },
        "alfonzo": {
            "spirit": [
                "phantom",
                "mouser",
                "dk_jumbo",
                "guts_man",
                "nibbles",
                "cammy",
                "diggernaut",
                "eggplant_wizard",
                "zebesian"
            ],
            "area": "none",
            "lock": "none"
        },
        "slippy_toad": {
            "spirit": [
                "jody_summer",
                "trace",
                "galaxy_man",
                "starmen",
                "wolfen",
                "starship_mario",
                "winged_aparoid",
                "luma",
                "magolor",
                "geno"
            ],
            "area": "none",
            "lock": "none"
        },
        "lapras": {
            "spirit": [
                "fishmen",
                "alolan_exeggutor",
                "emperor_bulblax",
                "cream_and_cheese",
                "ryota_hayami",
                "shantae",
                "tapu_koko",
                "rick",
                "alfonzo",
                "old_man_lobber"
            ],
            "area": "woods",
            "lock": "none"
        },
        "none": {
            "spirit": [],
            "area": "none",
            "lock": "none"
        }
    }
    global fighter_to_dlc
    fighter_to_dlc = {
        "jack_phantom_thief": [
            "jack_phantom_thieves",
            "jack_igor",
            "jack_caroline_justine",
            "jack_morgana",
            "jack_ryuji_sakamoto",
            "jack_anne_takamaki",
            "jack_yusuke_kitagawa",
            "jack_makoto_niijima",
            "jack_futaba_sakura",
            "jack_haru_okumura",
            "jack_goro_akechi"
        ],
        "brave_11": [
            "brave_group",
            "brave_cetacea",
            "brave_slime",
            "brave_king_slime",
            "brave_dracky",
            "brave_golem",
            "brave_baby_panther",
            "brave_killer_panther",
            "brave_liquid_metal"
        ],
        "buddy": [
            "buddy_tooty",
            "buddy_bottles",
            "buddy_mumbo_jumbo",
            "buddy_jinjo",
            "buddy_jinjonator",
            "buddy_jigsaw_piece",
            "buddy_gruntilda",
            "buddy_buzzbomb"
        ],
        "dolly": [
            "dolly_andy_bogard",
            "dolly_joe_higashi",
            "dolly_kim_kaphwan",
            "dolly_geese_howard",
            "dolly_ryo_sakazaki",
            "dolly_kyo_kusanagi",
            "dolly_iori_yagami",
            "dolly_haohmaru",
            "dolly_nakoruru",
            "dolly_athena_asamiya",
            "dolly_ralf_and_clark"
        ],
        "master_1": [
            "master_edelgard_1",
            "master_edelgard_2",
            "master_dimitri_1",
            "master_dimitri_2",
            "master_claude_1",
            "master_claude_2",
            "master_sothis",
            "master_rhea",
            "master_seteth",
            "master_dorothea",
            "master_ingrid",
            "master_hilda"
        ],
        "tantan_minmin": [
            "tantan_mastermummy",
            "tantan_mechanica",
            "tantan_byte_barq",
            "tantan_kidcobra",
            "tantan_helix",
            "tantan_maxbrass"
        ],
        "pickel_steve": [
            "pickel_zombie",
            "pickel_creeper",
            "pickel_skeleton",
            "pickel_slime",
            "pickel_enderman",
            "pickel_irongolem_villager",
            "pickel_ghast",
            "pickel_piglin",
            "pickel_enderdragon"
        ],
        "edge_sephiroth": [
            "edge_tifa",
            "edge_barret",
            "edge_aerith",
            "edge_red_xiii",
            "edge_cid",
            "edge_cait_sith",
            "edge_yuffie",
            "edge_vincent",
            "edge_turks_rufus",
            "edge_bahamut_zero",
            "edge_chocobo_moogle",
            "edge_shiva",
            "edge_ifrit"
        ],
        "element_homura": [
            "element_rex_2",
            "element_lora",
            "element_amalthus",
            "element_shin",
            "element_metsu",
            "element_puneuma"
        ],
        "element_hikari": [
            "element_rex_2",
            "element_lora",
            "element_amalthus",
            "element_shin",
            "element_metsu",
            "element_puneuma"
        ],
        "demon_kazuya_mishima_00": [
            "demon_heihachi_mishima",
            "demon_jin_kazama",
            "demon_devil_jin",
            "demon_kuma_panda",
            "demon_nina_williams",
            "demon_king_armor_king",
            "demon_ling_xiaoyu",
            "demon_paul_law",
            "demon_yoshimitsu",
            "demon_jack7",
            "demon_asuka_kazama"
        ],
        "trail_sora": [
            "trail_riku",
            "trail_kairi",
            "trail_roxas",
            "trail_axel",
            "trail_xion",
            "trail_terra",
            "trail_ventus",
            "trail_aqua"
        ]
    }
    global fighter_to_spot
    fighter_to_spot = {
        "piranha_plant":           ("light"               , "spot00210"),
        "jack_phantom_thief":      ("sub_006_base"        , "spot00013"),
        "brave_11":                ("sub_002_woods"       , "spot00137"),
        "buddy":                   ("light"               , "spot00183"),
        "dolly":                   ("light"               , "spot07754"),
        "master_1":                ("sub_014_dark_ganon"  , "spot00306"),
        "tantan_minmin":           ("sub_007_power_plant" , "spot00031"),
        "pickel_steve":            ("dark"                , "spot00025"),
        "edge_sephiroth":          ("sub_013_dark_marx"   , "spot00063"),
        "element_homura":          ("light"               , "spot07782"),
        "demon_kazuya_mishima_00": ("sub_015_dark_dracula", "spot00131"),
        "trail_sora":              ("light"               , "spot00159")
    }
    #Hash dictionaries
    for i in list(spirit_logic):
        spirit_logic[hash(i)] = spirit_logic.pop(i)
        for e in range(len(spirit_logic[hash(i)]["spirit"])):
            spirit_logic[hash(i)]["spirit"][e] = hash(spirit_logic[hash(i)]["spirit"][e])
        spirit_logic[hash(i)]["lock"] = hash(spirit_logic[hash(i)]["lock"])
    for i in list(fighter_to_dlc):
        fighter_to_dlc[hash(i)] = fighter_to_dlc.pop(i)
        for e in range(len(fighter_to_dlc[hash(i)])):
            fighter_to_dlc[hash(i)][e] = hash(fighter_to_dlc[hash(i)][e])

def load_param():
    global game_param
    game_param = {}
    for file in os.listdir("Data\\Param"):
        file_name = os.path.splitext(file)[0]
        game_param[file_name] = param(f"Data\\Param\\{file}")
    #Override any params that contains event spirit data
    if use_event_data:
        for file in os.listdir("Data\\Event\\Param"):
            file_name = os.path.splitext(file)[0]
            game_param[file_name] = param(f"Data\\Event\\Param\\{file}")

def load_text():
    global game_text
    game_text = {}
    if use_event_data:
        for file in os.listdir("Data\\Event\\Message"):
            file_name = os.path.splitext(file)[0]
            game_text[file_name] = ET.parse(f"Data\\Event\\Message\\{file}").getroot()

def load_json():
    global mod_data
    mod_data = {}
    #Open mod data
    for file_path in glob.glob("Data\\Json\\*.json"):
        file_name = os.path.split(os.path.splitext(file_path)[0])[-1]
        with open(file_path, "r", encoding="utf8") as file_reader:
            mod_data[file_name] = json.load(file_reader)
    for file_path in glob.glob("Data\\Json\\NewSpirit\\*.json"):
        file_name = os.path.split(os.path.splitext(file_path)[0])[-1]
        file_name = file_name.split(".")[-1]
        with open(file_path, "r", encoding="utf8") as file_reader:
            mod_data["CustomSpirit"][file_name] = json.load(file_reader)
    for file_path in glob.glob("Data\\Json\\NewBattle\\*.json"):
        file_name = os.path.split(os.path.splitext(file_path)[0])[-1]
        with open(file_path, "r", encoding="utf8") as file_reader:
            mod_data["CustomBattle"][file_name] = json.load(file_reader)
    #Convert all strings to hash
    for entry in list(mod_data["CustomBattle"]):
        mod_data["CustomBattle"][hash(entry)] = mod_data["CustomBattle"].pop(entry)
    for entry in list(mod_data["CustomSpirit"]):
        mod_data["CustomSpirit"][hash(entry)] = mod_data["CustomSpirit"].pop(entry)
        mod_data["CustomSpirit"][hash(entry)]["spirit_string"] = entry
    for entry in list(mod_data["FighterBattle"]):
        mod_data["FighterBattle"][hash(entry)] = mod_data["FighterBattle"].pop(entry)
    for entry in list(mod_data["BattleTweak"]):
        mod_data["BattleTweak"][hash(entry)] = mod_data["BattleTweak"].pop(entry)
    #Open text files
    mod_data["Skin"] = {}
    for file in os.listdir("Data\\Mod"):
        file_name = os.path.splitext(file)[0]
        character = f"ui_chara_{file_name}"
        mod_data["Skin"][hash(character)] = {}
        with open(f"Data\\Mod\\{file}", "r", encoding="utf8") as file_reader:
            lines = file_reader.readlines()
        for index in range(8):
            mod_data["Skin"][hash(character)][index] = int(lines[index].replace("c", "").strip())

def apply_default_tweaks():
    #FIGHTER
    #Some fighter battles are incomplete and need to be fixed
    #Battle data
    for entry in game_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        id = entry[hash("battle_id")].value
        if id in mod_data["FighterBattle"]:
            patch_param_entry(entry, mod_data["FighterBattle"][id], False)
            entry[hash("stage_type")].value    = hash("final_stage")
            entry[hash("item_table")].value    = hash("normal")
            entry[hash("item_level")].value    = hash("no_item")
            entry[hash("hint1_visible")].value = False
            entry[hash("hint2_visible")].value = False
            entry[hash("hint3_visible")].value = False
    #Enemy data
    for entry in game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = entry[hash("battle_id")].value
        if id in mod_data["FighterBattle"]:
            patch_param_entry(entry, mod_data["FighterBattle"][id], False)
            entry[hash("fly_rate")].value            = 1.0
            entry[hash("enable_charge_final")].value = True
            entry[hash("spirit_name")].value         = hash("none")
            entry[hash("ability1")].value            = hash("none")
            entry[hash("ability2")].value            = hash("none")
            entry[hash("ability3")].value            = hash("none")
    #CUSTOM
    #Apply custom spirits
    existing_spirits = []
    for entry in game_param["ui_spirit_db"][hash("db_root")]:
        id = entry[hash("ui_spirit_id")].value
        if id in mod_data["CustomSpirit"]:
            existing_spirits.append(id)
            patch_param_entry(entry, mod_data["CustomSpirit"][id], False)
            patch_text_entry("msg_spirits", "spi_" + mod_data["CustomSpirit"][id]["spirit_string"], mod_data["CustomSpirit"][id]["display_name"])
            change_directory_id(entry[hash("directory_id")].value, mod_data["CustomSpirit"][id]["spirit_slot"])
            fix_spirit_stand_pos(id, mod_data["CustomSpirit"][id]["center_x"], mod_data["CustomSpirit"][id]["center_y"])
            fix_spirit_effect_pos(id, hash(mod_data["CustomSpirit"][id]["similar_shape"]), mod_data["CustomSpirit"][id]["effect_offset_x"], mod_data["CustomSpirit"][id]["effect_offset_y"])
        #Make added spirit fights rematchable and non-enhanceable
        if id in mod_data["CustomBattle"]:
            entry[hash("evolve_src")].value        = hash("0")
            entry[hash("is_board_appear")].value   = True
            entry[hash("is_rematch_target")].value = True
    #If spirit doesn't exist then create it
    for entry in mod_data["CustomSpirit"]:
        if not entry in existing_spirits:
            add_new_spirit(entry)
    #Some spirits have no real battle assigned to them so they need to be fixed
    #Battle data
    for entry in game_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        id = entry[hash("battle_id")].value
        if id in mod_data["CustomBattle"]:
            patch_param_entry(entry, mod_data["CustomBattle"][id], False)
    #Enemy data
    #Add or remove enemy entries as needed
    new_list = []
    previous_id = ""
    for index in range(len(game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")])):
        current_id = game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")][index][hash("battle_id")].value
        if current_id == previous_id:
            count += 1
            if previous_id in mod_data["CustomBattle"]:
                if count > len(mod_data["CustomBattle"][previous_id]["enemy"]):
                    continue
        else:
            if previous_id in mod_data["CustomBattle"]:
                for subindex in range(len(mod_data["CustomBattle"][previous_id]["enemy"]) - count):
                    new_list.append(patch_param_entry(game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")][index - 1].clone(), mod_data["CustomBattle"][previous_id]["enemy"][count + subindex], True))
            count = 1
            previous_id = current_id
        if current_id in mod_data["CustomBattle"]:
            new_list.append(patch_param_entry(game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")][index], mod_data["CustomBattle"][current_id]["enemy"][count - 1], True))
        else:
            new_list.append(game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")][index])
    game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")].set_list(new_list)
    #TWEAK
    #Some existing spirits may need quick minor changes
    #Battle data
    for entry in game_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        id = entry[hash("battle_id")].value
        if id in mod_data["BattleTweak"]:
            patch_param_entry(entry, mod_data["BattleTweak"][id], False)
    #Enemy data
    for entry in game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = entry[hash("battle_id")].value
        #Only allow tweaks to the main enemy
        if entry[hash("entry_type")].value != hash("main_type"):
            continue
        if id in mod_data["BattleTweak"]:
            patch_param_entry(entry, mod_data["BattleTweak"][id], False)
    #Skin
    #Adapt the skin colors used in spirit battle to the user's mods
    for entry in game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = entry[hash("battle_id")].value
        if entry[hash("fighter_kind")].value in mod_data["Skin"] and not id in mod_data["FighterBattle"]:
            entry[hash("color")].value = mod_data["Skin"][entry[hash("fighter_kind")].value][entry[hash("color")].value]
    #MISC
    #Decrease downtime and slightly increase health on the true final boss so that it isn't easier than the standalone versions
    for boss in ["kiila", "darz"]:
        game_param[f"({boss})duet_param"][hash("max_hp")][hash("value_level_min")].value        = 450
        game_param[f"({boss})duet_param"][hash("max_hp")][hash("value_level_max")].value        = 1050
        game_param[f"({boss})duet_param"][hash("wait_time_min")][hash("value_level_min")].value = 150
        game_param[f"({boss})duet_param"][hash("wait_time_min")][hash("value_level_max")].value = 100
        game_param[f"({boss})duet_param"][hash("wait_time_max")][hash("value_level_min")].value = 220
        game_param[f"({boss})duet_param"][hash("wait_time_max")][hash("value_level_max")].value = 180

def add_new_spirit(spirit):
    has_battle = spirit in mod_data["CustomBattle"]
    #Only allow the spirit to use a middle slot if event spirits are in
    max_directory_id = 0
    for entry in game_param["ui_spirit_db"][hash("db_root")]:
        if entry[hash("directory_id")].value > max_directory_id:
            max_directory_id = entry[hash("directory_id")].value
    max_directory_id = max(max_directory_id, 1520) + 1
    if not use_event_data or mod_data["CustomSpirit"][spirit]["spirit_slot"] < 0:
        directory_id = max_directory_id
    else:
        directory_id = mod_data["CustomSpirit"][spirit]["spirit_slot"]
    #Append spirit entry
    param_list = list(game_param["ui_spirit_db"][hash("db_root")])
    param_list.append(param_list[0].clone())
    patch_param_entry(param_list[-1], mod_data["CustomSpirit"][spirit], False)
    param_list[-1][hash("ui_spirit_id")].value      = spirit
    param_list[-1][hash("name_id")].value           = mod_data["CustomSpirit"][spirit]["spirit_string"]
    param_list[-1][hash("save_no")].value           = max_directory_id - 1
    param_list[-1][hash("directory_id")].value      = max_directory_id
    param_list[-1][hash("is_board_appear")].value   = has_battle
    param_list[-1][hash("is_rematch_target")].value = has_battle
    game_param["ui_spirit_db"][hash("db_root")].set_list(param_list)
    change_directory_id(max_directory_id, directory_id)
    #Append layout entry
    param_list = list(game_param["ui_spirit_layout_db"][hash("db_root")])
    param_list.append(param_list[0].clone())
    param_list[-1][hash("ui_spirit_layout_id")].value = spirit
    game_param["ui_spirit_layout_db"][hash("db_root")].set_list(param_list)
    fix_spirit_stand_pos(spirit, mod_data["CustomSpirit"][spirit]["center_x"], mod_data["CustomSpirit"][spirit]["center_y"])
    fix_spirit_effect_pos(spirit, hash(mod_data["CustomSpirit"][spirit]["similar_shape"]), mod_data["CustomSpirit"][spirit]["effect_offset_x"], mod_data["CustomSpirit"][spirit]["effect_offset_y"])
    #Append battle entry
    param_list = list(game_param["ui_spirits_battle_db"][hash("battle_data_tbl")])
    param_list.append(param_list[0].clone())
    if has_battle:
        patch_param_entry(param_list[-1], mod_data["CustomBattle"][spirit], False)
    param_list[-1][hash("battle_id")].value = spirit
    game_param["ui_spirits_battle_db"][hash("battle_data_tbl")].set_list(param_list)
    #Append enemy entry
    param_list = list(game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")])
    if has_battle:
        for entry in mod_data["CustomBattle"][spirit]["enemy"]:
            param_list.append(param_list[0].clone())
            param_list[-1][hash("battle_id")].value = spirit
            patch_param_entry(param_list[-1], entry, True)
    else:
        param_list.append(param_list[0].clone())
        param_list[-1][hash("battle_id")].value = spirit
    game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")].set_list(param_list)
    #Append text entry
    patch_text_entry("msg_spirits", "spi_" + mod_data["CustomSpirit"][spirit]["spirit_string"], mod_data["CustomSpirit"][spirit]["display_name"])

def change_directory_id(old_slot, new_slot):
    if old_slot == new_slot:
        return
    #Change slot id and shift the value for all other spirits in between
    for entry in game_param["ui_spirit_db"][hash("db_root")]:
        if entry[hash("directory_id")].value == old_slot:
            entry[hash("directory_id")].value = new_slot
        elif new_slot < old_slot:
            if new_slot <= entry[hash("directory_id")].value < old_slot:
                entry[hash("directory_id")].value += 1
        elif new_slot > old_slot:
            if new_slot >= entry[hash("directory_id")].value > old_slot:
                entry[hash("directory_id")].value -= 1
    #Do it in the json too
    for entry in mod_data["CustomSpirit"]:
        if new_slot < old_slot:
            if new_slot <= mod_data["CustomSpirit"][entry]["spirit_slot"] < old_slot:
                mod_data["CustomSpirit"][entry]["spirit_slot"] += 1
        elif new_slot > old_slot:
            if new_slot >= mod_data["CustomSpirit"][entry]["spirit_slot"] > old_slot:
                mod_data["CustomSpirit"][entry]["spirit_slot"] -= 1

def fix_spirit_stand_pos(spirit, center_x, center_y):
    #Adjust the center point of a spirit image based on chosen image coordinates
    with open("Data\\Texture\\spirits_0_" + mod_data["CustomSpirit"][spirit]["spirit_string"] + ".bntx", "r+b") as file:
        file.seek(0x21C)
        width = int.from_bytes(file.read(2), "little")
        file.seek(0x220)
        height = int.from_bytes(file.read(2), "little")
    for entry in game_param["ui_spirit_layout_db"][hash("db_root")]:
        if entry[hash("ui_spirit_layout_id")].value == spirit:
            entry[hash("ui_art_on_stand_center_px_x")].value = round(width/2  - center_x)
            entry[hash("ui_art_on_stand_center_px_y")].value = round(center_y - height/2)
            entry[hash("ui_art_on_stand_scale")].value = 1
            entry[hash("ui_art_center_px_x")].value = entry[hash("ui_art_on_stand_center_px_x")].value - 5
            entry[hash("ui_art_center_px_y")].value = entry[hash("ui_art_on_stand_center_px_y")].value - 130
            entry[hash("ui_art_scale")].value = 1
            entry[hash("ui_art_type_under_center_px_x")].value = entry[hash("ui_art_on_stand_center_px_x")].value
            entry[hash("ui_art_type_under_center_px_y")].value = entry[hash("ui_art_on_stand_center_px_y")].value - 20
            entry[hash("ui_art_type_under_scale")].value = 1
            entry[hash("ui_art_chara_sel_center_px_x")].value = entry[hash("ui_art_on_stand_center_px_x")].value
            entry[hash("ui_art_chara_sel_center_px_y")].value = entry[hash("ui_art_on_stand_center_px_y")].value + 30
            entry[hash("ui_art_chara_sel_scale")].value = 1
            break

def fix_spirit_effect_pos(old_layout, new_layout, offset_x, offset_y):
    #Position graphical spirit effects based on another spirit of similar shape
    data = []
    for entry in game_param["ui_spirit_layout_db"][hash("db_root")]:
        if entry[hash("ui_spirit_layout_id")].value == new_layout:
            effect_num = entry[hash("effect_num")].value
            for index in range(15):
                data.append((entry[hash(f"effect_pos_{index}_x")].value, entry[hash(f"effect_pos_{index}_y")].value))
            break
    for entry in game_param["ui_spirit_layout_db"][hash("db_root")]:
        if entry[hash("ui_spirit_layout_id")].value == old_layout:
            entry[hash("effect_num")].value = effect_num
            for index in range(15):
                entry[hash(f"effect_pos_{index}_x")].value = data[index][0] + offset_x
                entry[hash(f"effect_pos_{index}_y")].value = data[index][1] + offset_y
            break

def gather_data():
    #List spirits
    for entry in game_param["ui_spirit_db"][hash("db_root")]:
        #Fill regular spirit list
        if (entry[hash("type")].value == hash("spirits_type_attack") or entry[hash("type")].value == hash("spirits_type_support")) and entry[hash("is_rematch_target")].value:
            spirit_list.append(entry[hash("ui_spirit_id")].value)
        #Get all summonable spirits
        if entry[hash("summon_sp")].value != 0:
            summonable.append(entry[hash("ui_spirit_id")].value)
        #Get all spirit indexes
        spirit_to_index[entry[hash("ui_spirit_id")].value] = entry[hash("save_no")].value
        #Get all spirit ranks
        spirit_to_rank[entry[hash("ui_spirit_id")].value]  = entry[hash("rank")].value
        #Get all spirit types
        spirit_to_type[entry[hash("ui_spirit_id")].value]  = entry[hash("type")].value
        #Get all spirit colors
        spirit_to_color[entry[hash("ui_spirit_id")].value] = entry[hash("attr")].value
    #Get all battle powers
    for entry in game_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        spirit_to_power[entry[hash("battle_id")].value] = entry[hash("battle_power")].value
    #Finalize logic list for light maps
    for param in game_param:
        if "map_param" in param and not "dark" in param:
            for entry in game_param[param][hash("map_spot_tbl")]:
                id = entry[hash("spirit")].value
                if id in spirit_list:
                    check = True
                    for key in spirit_logic:
                        #Is spirit already locked ?
                        if id in spirit_logic[key]["spirit"]:
                            check = False
                            break
                        #Is spirit in an area already locked ?
                        if spirit_logic[key]["area"] in param:
                            check = False
                            spirit_logic[key]["spirit"].append(id)
                    if check:
                        spirit_logic[hash("none")]["spirit"].append(id)

def rebalance_fs_meter():
    #Change the multipliers of the final smash meter to reward good performance rather than loss
    for entry in game_param["spirits_battle_level_param"][hash("charge_final_param")]:
        entry[hash("by_time_mul")].value   = 0
        entry[hash("by_attack_mul")].value = 5
        entry[hash("damage_mul")].value    = 0

def no_dlc_unlock():
    #Remove the auto unlock of DLC characters
    game_param["spirits_campaign_common_param"][hash("unlock_dlc_fighter_count")].value = 999

def shorten_final_boss():
    #Set the stage of the first fight to the boss rush one but without the bosses
    entry = get_param_entry_by_name(game_param["ui_spirits_battle_db"][hash("battle_data_tbl")], "battle_id", "final_stage1")
    entry[hash("battle_type")].value = hash("stock")
    entry[hash("ui_stage_id")].value = hash("ui_stage_boss_final2")
    entry[hash("stage_additional_setting")].value = 0
    #Tweak the enemies of the first fight to work properly
    entry = get_param_entry_by_name(game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")], "battle_id", "final_stage1")
    entry[hash("entry_type")].value   = hash("main_type")
    entry[hash("first_appear")].value = True
    entry[hash("cpu_lv")].value       = 100
    entry[hash("fly_rate")].value     = 1
    entry[hash("attack")].value       = 6200
    entry[hash("defense")].value      = 6200
    #Set the stage of the second fight to the same as the third and skip immediately
    entry = get_param_entry_by_name(game_param["ui_spirits_battle_db"][hash("battle_data_tbl")], "battle_id", "final_stage2")
    entry[hash("battle_type")].value = hash("stock")
    entry[hash("ui_stage_id")].value = hash("ui_stage_boss_final3")
    entry[hash("stage_additional_setting")].value = 0
    entry[hash("result_type")].value = hash("win_alive")
    entry[hash("battle_time_sec")].value = 1

def nerf_snacks():
    #Drastically reduce the exp given from snacks
    game_param["spirits_common"][hash(0x103a9abb0e)].value /= 5
    game_param["spirits_common"][hash(0x10fb1464ce)].value /= 5
    game_param["spirits_common"][hash(0x1007948b03)].value /= 5

def remove_dlc(fighter):
    #Remove DLC fighter from the pool
    fighter_skins = []
    found = False
    for entry in mod_data["FighterBattle"]:
        if entry == hash(fighter):
            fighter_skins.append(entry)
            found = True
        elif found:
            if mod_data["FighterBattle"][entry]["main_entry"]:
                break
            fighter_skins.append(entry)
    for entry in fighter_skins:
        del mod_data["FighterBattle"][entry]
    #Remove DLC spirit
    if hash(fighter) in fighter_to_dlc:
        for entry in fighter_to_dlc[hash(fighter)]:
            if entry in spirit_list:
                spirit_list.remove(entry)

def add_dlc_to_map(fighter):
    #Replace a chest by a DLC fighter
    map, spot = fighter_to_spot[fighter]
    for entry in game_param[f"spirits_campaign_map_param_{map}"][hash("map_spot_tbl")]:
        if entry[hash("hash")].value == hash(spot):
            entry[hash("type")].value         = hash("spot_type_fighter")
            entry[hash("spirit")].value       = hash(fighter)
            entry[hash("battle_id")].value    = hash("-1")
            entry[hash("sub_type")].value     = hash(0x16aa11d6c1 if "dark" in map else 0x17ada7e82e)
            entry[hash("item")].value         = hash("")
            entry[hash("model_degree")].value = 0

def randomize_spirit(fighter, spirit, master, boss):
    #Fighter
    fighter_dict = create_fighter_dict()
    values = list(fighter_dict.values())
    random.shuffle(values)
    fighter_replacement = dict(zip(fighter_dict, values))
    #Spirit
    values = [element for element in spirit_list]
    random.shuffle(values)
    spirit_replacement = dict(zip(spirit_list, values))
    #Master
    values = list(master_to_properties.keys())
    random.shuffle(values)
    master_replacement = dict(zip(master_to_properties, values))
    #Boss
    values = list(boss_to_properties.keys())
    random.shuffle(values)
    boss_replacement = dict(zip(boss_to_properties, values))
    #Place all information in a single dict
    if fighter:
        all_replacement.update(fighter_replacement)
    if spirit:
        all_replacement.update(spirit_replacement)
    if master:
        all_replacement.update(master_replacement)
    if boss:
        all_replacement.update(boss_replacement)
    #Invert dictionary
    all_replacement_invert.update({value: key for key, value in all_replacement.items()})

def create_fighter_dict():
    #Pick one skin to use per fighter
    old_fighter_pool = []
    new_fighter_pool = []
    fighter_alt      = []
    for entry in mod_data["FighterBattle"]:
        if mod_data["FighterBattle"][entry]["main_entry"]:
            old_fighter_pool.append(entry)
            if fighter_alt:
                new_fighter_pool.append(random.choice(fighter_alt))
            fighter_alt = [entry]
        else:
            fighter_alt.append(entry)
    #Do it one more time for the end of the file
    new_fighter_pool.append(random.choice(fighter_alt))
    return dict(zip(old_fighter_pool, new_fighter_pool))

def randomize_mii_specials():
    for entry in game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = entry[hash("battle_id")].value
        if id in [hash("mii_brawler_ssb"), hash("mii_swordfighter_ssb"), hash("mii_gunner_ssb")]:
            for direction in ["n", "s", "hi", "lw"]:
                entry[hash(f"mii_sp_{direction}")].value = random.randint(0, 2)

def patch_boss_entities():
    #Update sub boss placement
    for entry in game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        value = entry[hash("fighter_kind")].value
        if value in boss_to_properties:
            entry[hash("fighter_kind")].value = all_replacement[value]
    #Change Giga Bowser's stage to a standard walkoff as most bosses don't work on Final Destination
    #The best fit for this would be the result stage
    entry = get_param_entry_by_name(game_param["ui_spirits_battle_db"][hash("battle_data_tbl")], "battle_id", "giga_bawser")
    entry[hash("ui_stage_id")].value              = hash("ui_stage_result_stage")
    entry[hash("stage_additional_setting")].value = 0
    #This stage ID does not exist in vanilla so it needs to be created
    stage_list = list(game_param["ui_stage_db"][hash("db_root")])
    entry = get_param_entry_by_name(stage_list, "ui_stage_id", "ui_stage_setting_stage")
    stage_list.append(entry.clone())
    stage_list[-1][hash("ui_stage_id")].value           = hash("ui_stage_result_stage")
    stage_list[-1][hash("name_id")].value               = "ResultStage"
    stage_list[-1][hash("stage_place_id")].value        = hash("resultstage")
    stage_list[-1][hash("secret_stage_place_id")].value = hash("resultstage")
    game_param["ui_stage_db"][hash("db_root")].set_list(stage_list)
    #Increase Giga Bowser's size to make up for the bigger stage
    entry = get_param_entry_by_name(game_param["fighter_param"][hash("fighter_param_table")], "fighter_kind", "fighter_kind_koopag")
    entry[hash("scale")].value *= 1.5
    game_param["vl"][hash("param_special_n")][0][hash("fire_scale_min")].value *= 1.5
    game_param["vl"][hash("param_special_n")][0][hash("fire_scale_max")].value *= 1.5

def randomize_boss_gimmicks():
    split_dark_crazy_fights()
    #Assign gimmicks to each boss
    boss_to_gimmick = {}
    for boss_sublist in boss_list:
        entry = get_param_entry_by_name(game_param["ui_spirits_battle_db"][hash("battle_data_tbl")], "battle_id", boss_sublist[0])
        #Check gimmick compatibility
        valid_gimmicks = []
        for gimmick in mod_data["BossGimmick"]:
            if is_compatible_gimmick(gimmick, entry):
                valid_gimmicks.append(gimmick)
        chosen_gimmick = copy.deepcopy(random.choice(valid_gimmicks))
        #Only use different presets for the final stage
        if entry[hash("ui_stage_id")].value != hash("ui_stage_boss_final3"):
            if "floor_place_id" in chosen_gimmick:
                chosen_gimmick["floor_place_id"] = "preset1"
        for boss in boss_sublist:
            boss_to_gimmick[hash(boss)] = chosen_gimmick
    for entry in game_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        if entry[hash("battle_id")].value in boss_to_gimmick:
            patch_param_entry(entry, boss_to_gimmick[entry[hash("battle_id")].value], False)
    #Add text to some of the missing events
    patch_text_entry("msg_name", "nam_spirits_hint_rule_powerup_jump_up_player", "• You have increased jump power")
    patch_text_entry("msg_name", "nam_spirits_hint_rule_gravity_down_player", "• You are less affected by gravity")
    patch_text_entry("msg_name", "nam_spirits_hint_rule_speed_wild_player", "• You are very fast and can't stop quickly")
    patch_text_entry("msg_name", "nam_spirits_hint_rule_sleep_player", "• You are sleepy")
    patch_text_entry("msg_name", "nam_spirits_hint_rule_dark", "• The stage is shrouded in darkness")
    patch_text_entry("msg_name", "nam_spirits_rule_dark", "Dark Shift")
    #Add an entry for player jump up
    param_list = list(game_param["spirits_battle_event"][hash("powerup_param")])
    param_list.append(param_list[0].clone())
    param_list[-1][hash("label")].value            = hash("player_jump_up_l")
    param_list[-1][hash("is_player_target")].value = True
    param_list[-1][hash("is_enemy_target")].value  = False
    param_list[-1][hash("power_type")].value       = hash("jump")
    param_list[-1][hash("value")].value            = 8000
    game_param["spirits_battle_event"][hash("powerup_param")].set_list(param_list)
    #Add an entry for 300 damage
    param_list = list(game_param["spirits_battle_event"][hash("damage_param")])
    param_list.append(param_list[0].clone())
    param_list[-1][hash("label")].value            = hash("player_xl")
    param_list[-1][hash("is_player_target")].value = True
    param_list[-1][hash("is_enemy_target")].value  = False
    param_list[-1][hash("value")].value            = 300
    game_param["spirits_battle_event"][hash("damage_param")].set_list(param_list)
    #Add an entry for 300 heal
    param_list = list(game_param["spirits_battle_event"][hash("heal_param")])
    param_list.append(param_list[0].clone())
    param_list[-1][hash("label")].value            = hash("player_xl")
    param_list[-1][hash("is_player_target")].value = True
    param_list[-1][hash("is_enemy_target")].value  = False
    param_list[-1][hash("value")].value            = 300
    game_param["spirits_battle_event"][hash("heal_param")].set_list(param_list)

def is_compatible_gimmick(gimmick, battle_entry):
    #The true ending ignores all events for some reason
    if battle_entry[hash("battle_id")].value == hash("final_stage3"):
        for index in range(3):
            if f"event{index + 1}_type" in gimmick:
                return False
    return True

def split_dark_crazy_fights():
    #Make unique battle ids for the 3 crazy hand fights in the dark realm for gimmick rando
    #Act events
    param_list = list(game_param["spirits_campaign_act_param"][hash("act_tbl")])
    entry = get_param_entry_by_name(param_list, "hash", 0x134c238f64)
    for char in ['a', 'c']:
        param_list.append(entry.clone())
        param_list[-1][hash("hash")].value           = hash(f"dark_crazy_{char}_event_1")
        param_list[-1][hash("next_act_01")].value    = hash(f"dark_crazy_{char}_event_2")
    entry = get_param_entry_by_name(param_list, "hash", 0x16479b1010)
    for char in ['a', 'c']:
        param_list.append(entry.clone())
        param_list[-1][hash("hash")].value           = hash(f"dark_crazy_{char}_event_2")
        param_list[-1][hash("event_arg_hash")].value = hash(f"spot_crazy_{char}")
    game_param["spirits_campaign_act_param"][hash("act_tbl")].set_list(param_list)
    #Battle spots
    param_list = list(game_param["spirits_campaign_map_param_dark"][hash("map_spot_tbl")])
    entry = get_param_entry_by_name(param_list, "hash", "spot_crazy_b")
    for char in ['a', 'c']:
        param_list.append(entry.clone())
        param_list[-1][hash("hash")].value      = hash(f"spot_crazy_{char}")
        param_list[-1][hash("label")].value     = f"SPOT_CRAZY_{char.upper()}"
        param_list[-1][hash("battle_id")].value = hash(f"crazy_hand_{char}")
    game_param["spirits_campaign_map_param_dark"][hash("map_spot_tbl")].set_list(param_list)
    #Barrier spots
    for entry in game_param["spirits_campaign_map_param_dark"][hash("map_spot_tbl")]:
        if entry[hash("hash")].value in [hash("spot_boss_crazy_pos_01"), hash("spot_boss_crazy_pos_01_b"), hash("spot_boss_crazy_pos_01_c"), hash("spot_boss_crazy_pos_02"), hash("spot_boss_crazy_pos_02_b")]:
            for index in range(5):
                parameter = hash("chain_clear_spot_" + "{:02d}".format(index + 1))
                if entry[parameter].value == hash("spot_crazy_b"):
                    entry[parameter].value = hash("spot_crazy_a")
            entry[hash("act_hash_decide")].value = hash("dark_crazy_a_event_1")
        if entry[hash("hash")].value in [hash("spot_boss_crazy_pos_05"), hash("spot_boss_crazy_pos_05_b"), hash("spot_boss_crazy_pos_05_c")]:
            for index in range(5):
                parameter = hash("chain_clear_spot_" + "{:02d}".format(index + 1))
                if entry[parameter].value == hash("spot_crazy_b"):
                    entry[parameter].value = hash("spot_crazy_c")
            entry[hash("act_hash_decide")].value = hash("dark_crazy_c_event_1")
    #Battle data
    for char in ['a', 'c']:
        param_list = list(game_param["ui_spirits_battle_db"][hash("battle_data_tbl")])
        entry = get_param_entry_by_name(param_list, "battle_id", "crazy_hand")
        param_list.append(entry.clone())
        param_list[-1][hash("battle_id")].value = hash(f"crazy_hand_{char}")
        game_param["ui_spirits_battle_db"][hash("battle_data_tbl")].set_list(param_list)
        param_list = list(game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")])
        entry = get_param_entry_by_name(param_list, "battle_id", "crazy_hand")
        param_list.append(entry.clone())
        param_list[-1][hash("battle_id")].value = hash(f"crazy_hand_{char}")
        game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")].set_list(param_list)

def randomize_skill():
    #Get all skill data as tuples
    data = []
    for entry in game_param["ui_campaign_skill_db"][hash("db_root")]:
        if entry[hash("spirits_ability_id")].value != hash("none"):
            data.append((
                entry[hash("node_index")].value      ,
                entry[hash("connection0")].value     ,
                entry[hash("connection1")].value     ,
                entry[hash("connection2")].value     ,
                entry[hash("connection3")].value     ,
                entry[hash("connection4")].value     ,
                entry[hash("connection_count")].value
            ))
    #Reassign data at random
    for entry in game_param["ui_campaign_skill_db"][hash("db_root")]:
        if entry[hash("spirits_ability_id")].value != hash("none"):
            chosen = pick_and_remove(data)
            entry[hash("node_index")].value       = chosen[0]
            entry[hash("connection0")].value      = chosen[1]
            entry[hash("connection1")].value      = chosen[2]
            entry[hash("connection2")].value      = chosen[3]
            entry[hash("connection3")].value      = chosen[4]
            entry[hash("connection4")].value      = chosen[5]
            entry[hash("connection_count")].value = chosen[6]

def rebalance_spirit(boss):
    #SPIRIT
    for entry in game_param["ui_spirit_db"][hash("db_root")]:
        #Check ID and evolve from
        id     = entry[hash("ui_spirit_id")].value
        origin = entry[hash("evolve_src")].value
        #Get multiplier and rank
        if boss and id in spirit_to_boss:
            #Get rank difference between original and replacement
            difference = boss_to_properties[all_replacement_invert[spirit_to_boss[id]]][2] - boss_to_properties[spirit_to_boss[id]][2]
            star_num   = rank_to_star[spirit_to_rank[id]] + difference
        elif not id in all_replacement_invert and not origin in all_replacement_invert:
            continue
        elif origin == hash("0"):
            star_num = rank_to_star[spirit_to_rank[all_replacement_invert[id]]]
        else:
            #Get rank difference between original and upgraded
            difference = rank_to_star[spirit_to_rank[id]] - rank_to_star[spirit_to_rank[origin]]
            star_num   = rank_to_star[spirit_to_rank[all_replacement_invert[origin]]] + difference
            #Stars must be in range
            star_num = max(min(star_num, 4), 1)
        #Change rank
        entry[hash("rank")].value = rank_to_star_invert[star_num]
        #Base fighter and master spirits on battle power
        if id in mod_data["FighterBattle"] or id in master_to_properties:
            multiplier = spirit_to_power[all_replacement_invert[id]]/spirit_to_power[id]
        #Base regular spirits on rank
        else:
            multiplier = rank_to_intensity[entry[hash("rank")].value]/rank_to_intensity[spirit_to_rank[id]]
        #Multiply spirit stats
        if entry[hash("type")].value         == hash("spirits_type_attack"):
            entry[hash("base_attack")].value  = round(entry[hash("base_attack")].value  * multiplier ** 0.6)
            entry[hash("max_attack")].value   = round(entry[hash("max_attack")].value   * multiplier ** 0.6)
            entry[hash("base_defense")].value = round(entry[hash("base_defense")].value * multiplier ** 0.6)
            entry[hash("max_defense")].value  = round(entry[hash("max_defense")].value  * multiplier ** 0.6)
        #Make sure stats don't exceed the max
        entry[hash("max_attack")].value  = min(entry[hash("max_attack")].value,  10000)
        entry[hash("max_defense")].value = min(entry[hash("max_defense")].value, 10000)
        #Other properties
        entry[hash("reward_capacity")].value = round(entry[hash("reward_capacity")].value * multiplier ** 1.25)
        entry[hash("exp_lv_max")].value      = round(entry[hash("exp_lv_max")].value      * multiplier ** 0.88)
        entry[hash("battle_exp")].value      = round(entry[hash("battle_exp")].value      * multiplier ** 0.5)
        entry[hash("shop_price")].value      = round(entry[hash("shop_price")].value      * multiplier ** 1.8)
        #Make stats multiples of specific numbers                                                                     
        entry[hash("exp_lv_max")].value = round(entry[hash("exp_lv_max")].value/5)  *5
        entry[hash("battle_exp")].value = round(entry[hash("battle_exp")].value/50) *50
        entry[hash("shop_price")].value = round(entry[hash("shop_price")].value/500)*500
        #Get fallback battle ID in case there is one
        if entry[hash("replace_battle_id")].value != hash(""):
            spirit_override[entry[hash("replace_battle_id")].value] = id
    #BATTLE
    for entry in game_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        #Check ID with potential override
        if entry[hash("battle_id")].value in spirit_override:
            id = spirit_override[entry[hash("battle_id")].value]
        else:
            id = entry[hash("battle_id")].value
        #Skip if not randomized
        if not id in all_replacement_invert:
            continue
        #Base fighter and master spirits on battle power
        if id in mod_data["FighterBattle"] or id in master_to_properties:
            multiplier = spirit_to_power[all_replacement_invert[id]]/spirit_to_power[id]
        #Base regular spirit on rank
        else:
            multiplier = rank_to_intensity[spirit_to_rank[all_replacement_invert[id]]]/rank_to_intensity[spirit_to_rank[id]]
        #Multiply battle stats
        entry[hash("battle_power")].value = round(entry[hash("battle_power")].value * multiplier ** 1.0)
        #Make stats multiples of specific numbers
        entry[hash("battle_power")].value = round(entry[hash("battle_power")].value/100)*100
    #FIGHTER
    for entry in game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        #Check ID with potential override
        if entry[hash("battle_id")].value in spirit_override:
            id = spirit_override[entry[hash("battle_id")].value]
        else:
            id = entry[hash("battle_id")].value
        #Skip if not randomized
        if not id in all_replacement_invert:
            continue
        #Base fighter and master spirits on battle power
        if id in mod_data["FighterBattle"] or id in master_to_properties:
            multiplier = spirit_to_power[all_replacement_invert[id]]/spirit_to_power[id]
        #Base regular spirit on rank
        else:
            multiplier = rank_to_intensity[spirit_to_rank[all_replacement_invert[id]]]/rank_to_intensity[spirit_to_rank[id]]
        #Multiply enemy stats
        attack      = round(entry[hash("attack")].value  * multiplier ** 1.0)
        defense     = round(entry[hash("defense")].value * multiplier ** 1.2)
        cpu_lv      = round(entry[hash("cpu_lv")].value  * multiplier ** 0.56)
        #Make stats multiples of specific numbers
        attack      = round(attack/50) *50
        defense     = round(defense/50)*50
        #Make sure stats don't exceed the max
        attack  = min(attack,  10000)
        defense = min(defense, 10000)
        cpu_lv  = min(cpu_lv,    100)
        #Patch values
        entry[hash("attack")].value  = attack
        entry[hash("defense")].value = defense
        entry[hash("cpu_lv")].value  = cpu_lv

def shorten_playthrough(length):
    #Create shorter playthroughs by removing spirit spots at random
    irrelevent = [
        hash(""),
        hash("spot_blind_flag_002"),
        hash("spot_blind_flag_013"),
        hash("spot_blind_flag_004"),
        hash("spot_blind_flag_020")
    ]
    remove_list = []
    keep_list   = []
    for param in game_param:
        if "map_param" in param:
            important   = []
            tutorial    = []
            if param == "spirits_campaign_map_param_light":
                #One spot to uncover all clouds
                important.append(hash("sp01_02"))
                for entry in game_param[param][hash("map_blind_tbl")]:
                    entry[hash("chain_spot_01")].value = hash("sp01_02")
                    for index in range(9):
                        entry[hash("chain_spot_" + "{:02d}".format(index + 2))].value = hash("")
                #Button prompt tutorials
                tutorial.append(hash("sp01_01"))
                tutorial.append(hash("fig01_01"))
                tutorial.append(hash("fig01_02"))
                tutorial.append(hash("fig01_03"))
                tutorial.append(hash("fig01_04"))
            if param == "spirits_campaign_map_param_dark":
                #One spot to uncover all top clouds
                important.append(hash("sp52_01"))
                for index in range(7):
                    game_param[param][hash("map_blind_tbl")][index][hash("chain_spot_01")].value = hash("sp52_01")
                    for subindex in range(9):
                        game_param[param][hash("map_blind_tbl")][index][hash("chain_spot_" + "{:02d}".format(subindex + 2))].value = hash("")
                #One spot to uncover all left clouds
                important.append(hash("sp53_01"))
                for index in range(5):
                    game_param[param][hash("map_blind_tbl")][index + 7][hash("chain_spot_01")].value = hash("sp53_01")
                    for subindex in range(9):
                        game_param[param][hash("map_blind_tbl")][index + 7][hash("chain_spot_" + "{:02d}".format(subindex + 2))].value = hash("")
                #One spot to uncover all right clouds
                important.append(hash("sp_54_01"))
                for index in range(5):
                    game_param[param][hash("map_blind_tbl")][index + 7 + 5][hash("chain_spot_01")].value = hash("sp_54_01")
                    for subindex in range(9):
                        game_param[param][hash("map_blind_tbl")][index + 7 + 5][hash("chain_spot_" + "{:02d}".format(subindex + 2))].value = hash("")
            #Remove spirits spots for shorter length
            for entry in game_param[param][hash("map_spot_tbl")]:
                id = entry[hash("spirit")].value
                remove = False
                #Determine if the spirit must be removed
                if id in keep_list:
                    pass
                elif id in remove_list:
                    remove = True
                elif random.randint(1, 5) <= length:
                    pass
                elif entry[hash("hash")].value in important:
                    pass
                elif id in mod_data["FighterBattle"] or id in spirit_list or id in master_to_properties:
                    remove = True
                #Proceed
                if remove:
                    #Remove spirit from logic
                    for key in spirit_logic:
                        if id in spirit_logic[key]["spirit"]:
                            spirit_logic[key]["spirit"].remove(id)
                    #Remove spirit from map
                    entry[hash("type")].value = hash("spot_type_space")
                    #Keep a random food item if the spirit spawns from event
                    if entry[hash(0x1849e18674)].value in irrelevent:
                        entry[hash("sub_type")].value = hash("")
                    else:
                        entry[hash("sub_type")].value = hash(random.choice(food_type))
                    #Disable the last map event
                    if entry[hash("act_hash_clear")].value == hash(0x1838832598):
                        entry[hash("act_hash_clear")].value = hash("")
                    #Remove the button promptfor the few tutorial spots
                    if entry[hash("hash")].value in tutorial:
                        entry[hash("act_hash_decide")].value = hash("")
                    #Remove corresponding master activity too
                    if id in master_to_properties:
                        for index in master_to_properties[id][1]:
                            game_param[param][hash("map_spot_tbl")][index][hash("sub_type")].value = hash("")
                    #Keep spirit status in memory
                    remove_list.append(id)
                else:
                    keep_list.append(id)

def patch_spot():
    #Apply shuffled changes to all spirit spots
    for param in game_param:
        if "map_param" in param:
            for entry in game_param[param][hash("map_spot_tbl")]:
                id = entry[hash("spirit")].value
                #Change spirit
                if id in all_replacement:
                    entry[hash("spirit")].value    = all_replacement[id]
                    entry[hash("battle_id")].value = hash("-1")
                    entry[hash("item")].value      = hash("")
                    #Change the corresponding activity spots for master spirits
                    if entry[hash("type")].value == hash("spot_type_build"):
                        entry[hash("sub_type")].value = master_to_properties[all_replacement[id]][0]
                        for index in master_to_properties[id][1]:
                            game_param[param][hash("map_spot_tbl")][index][hash("sub_type")].value = master_to_properties[all_replacement[id]][2]
                #Change the corresponding rewards for boss characters
                if id in boss_to_properties_invert:
                    if boss_to_properties_invert[id] in all_replacement:
                        #Battle ID must remain the same
                        if entry[hash("battle_id")].value == hash("-1"):
                            entry[hash("battle_id")].value = id
                        entry[hash("spirit")].value = boss_to_properties[all_replacement[boss_to_properties_invert[id]]][0]
                        entry[hash("item")].value   = boss_to_properties[all_replacement[boss_to_properties_invert[id]]][1]

def randomize_rewards():
    skip_list = []
    for index in range(10):
        skip_list.append(hash("spirit_" + "{:02d}".format(index + 1)))
    #Randomize standard pickups found in chests
    for param in game_param:
        if "map_param" in param:
            for entry in game_param[param][hash("map_spot_tbl")]:
                if entry[hash("type")].value == hash("spot_type_item") and not entry[hash("item")].value in skip_list:
                    entry[hash("item")].value = hash(random.choice(reward_type))

def patch_requirement(spirit):
    #Determine logic behind key spirits
    barrier = list(spirit_logic)
    barrier.remove(hash("none"))
    random.shuffle(barrier)
    #If a barrier doesn't lock anything append it at the end
    for key in spirit_logic:
        if key == hash("none"):
            continue
        if not spirit_logic[key]["spirit"]:
            barrier.remove(key)
            barrier.append(key)
    #Assign keys
    for key in barrier:
        spirit_logic[key]["key"] = pick_and_remove(spirit_logic[hash("none")]["spirit"])
        #Checking if barrier is locked behind another barrier
        if spirit_logic[spirit_logic[key]["lock"]]["spirit"]:
            lock = spirit_logic[key]["lock"]
        else:
            lock = hash("none")
        spirit_logic[lock]["spirit"].extend(spirit_logic[key]["spirit"])
        spirit_logic[lock]["spirit"] = list(dict.fromkeys(spirit_logic[lock]["spirit"]))
        spirit_logic[key]["spirit"].clear()
    #Change blockade spirit requirements to reflect the logic
    for entry in game_param["spirits_campaign_barrier_param"][hash("barrier_tbl")]:
        id = entry[hash("spirit_01")].value
        if id == hash(""):
            continue
        key = spirit_logic[id]["key"]
        entry[hash("spirit_01")].value = all_replacement[key] if spirit else key
        for index in range(9):
            entry[hash("spirit_" + "{:02d}".format(index + 2))].value = hash("")

def patch_reward():
    #Change spirits that are found directly in chests
    for entry in game_param["spirits_campaign_item_param"][hash("item_tbl")]:
        id = entry[hash("key")].value
        if id in all_replacement:
            entry[hash("key")].value = all_replacement[id]

def patch_shop():
    #Change spirits that are sold at the shops
    for index in range(5):
        for entry in game_param["ui_shop_db"][hash(f"shop_spirit_adv_{index + 1}")]:
            id = entry[hash("ui_spirit_id")].value
            if id in all_replacement:
                entry[hash("ui_spirit_id")].value = all_replacement[id]

def patch_summon():
    #Replace summonable spirits and randomize their requirements
    #Create lists
    item_num_list   = [2, 2, 2, 3, 3, 4]
    common_list = [
        hash("common_none"),
        hash("common_spt"),
        hash("common_atk"),
        hash("common_def"),
        hash("common_trw")
    ]
    common_num_list      = [0, 0, 0, 0, 1, 1, 1, 2, 2, 3]
    common_quantity_list = [1, 1, 1, 1, 1, 1, 1, 2, 2, 3]
    #Change spirits that are summonable
    for entry in game_param["ui_spirit_db"][hash("db_root")]:
        id = entry[hash("ui_spirit_id")].value
        if not id in all_replacement_invert:
            continue
        if all_replacement_invert[id] in summonable:
            #Get number of items required
            item_num   = random.choice(item_num_list)
            common_num = random.choice(common_num_list)
            #Make sure that there is at least one normal spirit
            while common_num > item_num - 1:
                common_num = random.choice(common_num_list)
            #Patch entries
            for index in range(5):
                if index < item_num - common_num:
                    entry[hash(f"summon_item{index + 1}")].value     = random.choice(spirit_list)
                    entry[hash(f"summon_item{index + 1}_num")].value = 1
                elif index < item_num:
                    entry[hash(f"summon_item{index + 1}")].value     = random.choice(common_list)
                    entry[hash(f"summon_item{index + 1}_num")].value = random.choice(common_quantity_list)
                else:
                    entry[hash(f"summon_item{index + 1}")].value     = hash("none")
                    entry[hash(f"summon_item{index + 1}_num")].value = 0
        else:
            #Make the rest non-summonable
            for index in range(5):
                entry[hash(f"summon_item{index + 1}")].value     = hash("none")
                entry[hash(f"summon_item{index + 1}_num")].value = 0

def patch_master_element():
    #Change master spirit spot elements based on their new location
    for entry in game_param["spirits_campaign_resource_param"][hash(0x11a29ee536)]:
        id = entry[hash("type_sub")].value
        if id in master_to_properties_invert:
            element = master_to_properties[all_replacement_invert[master_to_properties_invert[id]]][3]
            entry[hash("obj_model_resource_name")].value       = hash(f"point_spirit_{element}_on")
            entry[hash("obj_model_resource_name_clear")].value = hash(f"point_spirit_{element}_off")
            entry[hash("obj_effect_hash")].value               = hash(f"cp_map_{element}spirits")
            entry[hash("obj_effect_hash_out")].value           = hash(f"cp_map_{element}spirits_release")
    #This however does not affect the intro animations, maybe those are hardcoded

def patch_param_entry(entry, data, special):
    for subdata in data:
        try:
            entry[hash(subdata)].value = hash(data[subdata]) if type(data[subdata]) is str else data[subdata]
        except IndexError:
            continue
    if special:
        entry[hash("spirit_name")].value = entry[hash("battle_id")].value if data["use_spirit"] else hash("none")
    return entry

def patch_text_entry(file, entry, text):
    #Create msbt patches directly when changing a string entry
    try:
        game_text[file]
    except KeyError:
        game_text[file] = ET.Element("xmsbt")
    entry = ET.SubElement(game_text[file], "entry", label=entry)
    ET.SubElement(entry, "text").text = text

def save_param(path):
    for param in game_param:
        game_param[param].save(path + "\\" + mod_data["FileToPath"][param] + "\\" + param.split(")")[-1] + ".prc")

def save_floor(path):
    for item in os.listdir("Data\\Floor"):
        if os.path.isfile(f"Data\\Floor\\{item}"):
            shutil.copyfile(f"Data\\Floor\\{item}", f"{path}\\{item}")
        if os.path.isdir(f"Data\\Floor\\{item}"):
            shutil.copytree(f"Data\\Floor\\{item}", f"{path}\\{item}", dirs_exist_ok=True)

def save_text(path):
    for text in game_text:
        tree = minidom.parseString(ET.tostring(game_text[text])).toprettyxml(encoding="utf-16", indent="    ")
        with open(f"{path}\\ui\\message\\{text}.xmsbt", "wb") as filewriter:
            filewriter.write(tree)

def save_texture(path):
    #Copy spirit UIs to mod folder
    param_list = [("Texture", "replace")]
    if use_event_data:
        param_list.append(("Event\\Texture", "replace_patch"))
    for input, output in param_list:
        spirit_images = []
        for file in os.listdir(f"Data\\{input}"):
            file_name = os.path.splitext(file)[0]
            spirit_images.append(file_name.replace("spirits_0_", "").replace("spirits_1_", "").replace("spirits_2_", ""))
        spirit_images = list(dict.fromkeys(spirit_images))
        for image in spirit_images:
            for index in range(3):
                shutil.copyfile(f"Data\\{input}\\spirits_{index}_{image}.bntx", f"{path}\\ui\\{output}\\spirits\\spirits_{index}\\spirits_{index}_{image}.bntx")
    #To make outlines:
    #Image dimensions x0.55
    #Content dimensions x0.9
    #Drop shadow grow radius 1
    #Gaussian blur 1.25

def convert_param_to_patch(path):
    for param in game_param:
        vanilla_file = f"Data\\Param\\{param}.prc"
        modded_file = path + "\\" + mod_data["FileToPath"][param] + "\\" + param.split(")")[-1] + ".prc"
        os.system(f"cmd /c parcel diff \"{vanilla_file}\" \"{modded_file}\" \"{modded_file}x\"")
        os.remove(modded_file)

def reset_spirit(path):
    with open(path, "r+b") as file:
        #Spirits
        file.seek(0x43471C)
        for index in range(6000):
            file.write((0xFFFFFFFF).to_bytes(4, "little"))
            file.write((0).to_bytes(6, "little"))
            file.write((0xFFFF).to_bytes(2, "little"))
            file.write((0).to_bytes(40, "little"))
        #Activities
        #Seems jank so disable it for now
        #file.seek(0xD4)
        #file.write((0).to_bytes(252, "little"))
        #Cores
        file.seek(0x426C5C)
        for index in range(2000):
            file.write((0).to_bytes(26, "little"))
            #Skip the collection unlock
            file.read(1)
            file.write((0).to_bytes(1, "little"))
        #Gold
        file.seek(0x5506DC)
        file.write((0).to_bytes(4, "little"))
        #SP
        file.seek(0x4831E4)
        file.write((0).to_bytes(4, "little"))
        #Snacks
        file.seek(0x4831CE)
        file.write((0).to_bytes(2, "little"))
        file.seek(0x4831D0)
        file.write((0).to_bytes(2, "little"))
        file.seek(0x4831D2)
        file.write((0).to_bytes(2, "little"))
        #Spirit board items
        file.seek(0x4831C0)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831C1)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831C2)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831C4)     
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831C3)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831C6)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831C7)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831C8)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831C9)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831CA)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831CB)
        file.write((0).to_bytes(1, "little"))
        file.seek(0x4831CC)
        file.write((0).to_bytes(1, "little"))

def start_spirit(path):
    #Determine starting spirits
    spirit_in_wol = get_spirits_in_wol()
    start_spirits = []
    spirit_pool = [element for element in spirit_list]
    #One primary of each color
    for attr in ["atk", "def", "trw"]:
        chosen = random.choice(spirit_pool)
        while get_current_rank(chosen) != hash("hope") or spirit_to_type[chosen] != hash("spirits_type_attack") or spirit_to_color[chosen] != hash(f"spirits_attr_{attr}") or chosen in spirit_in_wol:
            chosen = random.choice(spirit_pool)
        spirit_pool.remove(chosen)
        start_spirits.append(chosen)
    #Three supports
    for index in range(3):
        chosen = random.choice(spirit_pool)
        while get_current_rank(chosen) != hash("hope") or spirit_to_type[chosen] != hash("spirits_type_support") or chosen in spirit_in_wol:
            chosen = random.choice(spirit_pool)
        spirit_pool.remove(chosen)
        start_spirits.append(chosen)
    #Open save
    with open(path, "r+b") as file:
        #Put spirits in inventory
        file.seek(0x43471C)
        for index in range(len(start_spirits)):
            file.write(index.to_bytes(4, "little"))
            file.write((0).to_bytes(6, "little"))
            file.write(spirit_to_index[start_spirits[index]].to_bytes(2, "little"))
            file.write((0).to_bytes(4, "little"))
            file.write((0xFF0E).to_bytes(2, "little"))
            file.write((0).to_bytes(34, "little"))
        #Unlock them in collection
        for index in range(len(start_spirits)):
            file.seek(0x426C5C + spirit_to_index[start_spirits[index]]*0x1C + 0x1A)
            file.write((0x0D).to_bytes(1, "little"))

def get_param_entry_by_name(param_list, parameter, name):
    for entry in param_list:
        if entry[hash(parameter)].value == hash(name):
            return entry
    raise Exception(f"No entry matches parameter name {name}")

def get_spirits_in_wol():
    #Get a list of the spirits that can be obtained through WoL
    list = []
    #Map spirits
    for param in game_param:
        if "map_param" in param:
            for entry in game_param[param][hash("map_spot_tbl")]:
                if entry[hash("type")].value == hash("spot_type_spirit"):
                    list.append(entry[hash("spirit")].value)
    #Chest spirits
    for entry in game_param["spirits_campaign_item_param"][hash("item_tbl")]:
        id = entry[hash("key")].value
        if id in spirit_list:
            list.append(id)
    #Summonable spirits
    for entry in game_param["ui_spirit_db"][hash("db_root")]:
        if entry[hash("summon_item1")].value != hash("none"):
            list.append(entry[hash("ui_spirit_id")].value)
    #Shop spirits
    for index in range(5):
        for entry in game_param["ui_shop_db"][hash(f"shop_spirit_adv_{index + 1}")]:
            id = entry[hash("ui_spirit_id")].value
            if id in spirit_list:
                list.append(id)
    return list

def get_current_rank(spirit):
    try:
        return spirit_to_rank[all_replacement_invert[spirit]]
    except KeyError:
        return spirit_to_rank[spirit]

def pick_and_remove(array):
    item = random.choice(array)
    array.remove(item)
    return item

def average_check(rank):
    #Debug function
    count = 0
    max_attack = 0
    max_defense = 0
    reward_capacity = 0
    exp_lv_max = 0
    battle_exp = 0
    shop_price = 0
    for i in game_param["ui_spirit_db"][hash("db_root")]:
        id = i[hash("ui_spirit_id")].value
        if id in spirit_list and spirit_to_rank[id] == hash(rank):
            count += 1
            max_attack += i[hash("max_attack")].value
            max_defense += i[hash("max_defense")].value
            reward_capacity += i[hash("reward_capacity")].value
            exp_lv_max += i[hash("exp_lv_max")].value
            battle_exp += i[hash("battle_exp")].value
            shop_price += i[hash("shop_price")].value
    max_attack /= count
    max_defense /= count
    reward_capacity /= count
    exp_lv_max /= count
    battle_exp /= count
    shop_price /= count
    
    count = 0
    battle_power = 0
    for i in game_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        id = i[hash("battle_id")].value
        if id in spirit_list and spirit_to_rank[id] == hash(rank):
            count += 1
            battle_power += i[hash("battle_power")].value
    battle_power /= count
    
    count = 0
    attack = 0
    defense = 0
    cpu_lv = 0
    for i in game_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = i[hash("battle_id")].value
        if id in spirit_list and spirit_to_rank[id] == hash(rank):
            count += 1
            attack += i[hash("attack")].value
            defense += i[hash("defense")].value
            cpu_lv += i[hash("cpu_lv")].value
    attack /= count
    defense /= count
    cpu_lv /= count
    
    print(f"max_attack {max_attack}")
    print(f"max_defense {max_defense}")
    print(f"reward_capacity {reward_capacity}")
    print(f"exp_lv_max {exp_lv_max}")
    print(f"battle_exp {battle_exp}")
    print(f"shop_price {shop_price}")
    print(f"battle_power {battle_power}")
    print(f"attack {attack}")
    print(f"defense {defense}")
    print(f"cpu_lv {cpu_lv}")