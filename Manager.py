from pyprc import *
import os
import shutil
import random
import json
import xml.etree.cElementTree as ET
from xml.dom import minidom

#hash.load_labels("ParamLabels.csv")

def init_variable():
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
    rank_to_star_invert = {}
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
    boss_to_properties_invert = {}
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
    master_to_properties_invert = {}
    global all_replacement
    all_replacement = {}
    global all_replacement_invert
    all_replacement_invert = {}
    global all_text
    all_text = {}
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
    #Invert dictionaries
    for i in rank_to_star:
        rank_to_star_invert[rank_to_star[i]] = i
    for i in boss_to_properties:
        boss_to_properties_invert[boss_to_properties[i][0]] = i
    for i in master_to_properties:
        master_to_properties_invert[master_to_properties[i][0]] = i
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
    global all_param
    all_param = {}
    for i in os.listdir("Data\\Param"):
        name, extension = os.path.splitext(i)
        all_param[name] = param("Data\\Param\\" + i)

def load_json():
    global all_json
    all_json = {}
    for i in os.listdir("Data\\Json"):
        name, extension = os.path.splitext(i)
        with open("Data\\Json\\" + i, "r", encoding="utf8") as file_reader:
            all_json[name] = json.load(file_reader)
    #Convert all strings to hash
    for i in list(all_json["CustomBattle"]):
        all_json["CustomBattle"][hash(i)] = all_json["CustomBattle"].pop(i)
    for i in list(all_json["CustomSpirit"]):
        all_json["CustomSpirit"][hash(i)] = all_json["CustomSpirit"].pop(i)
        all_json["CustomSpirit"][hash(i)]["spirit_string"] = i
    for i in list(all_json["Fighter"]):
        all_json["Fighter"][hash(i)] = all_json["Fighter"].pop(i)
    for i in list(all_json["TweakBattle"]):
        all_json["TweakBattle"][hash(i)] = all_json["TweakBattle"].pop(i)
    #Open text files
    all_json["Skin"] = {}
    for i in os.listdir("Data\\Mod"):
        name, extension = os.path.splitext(i)
        character = "ui_chara_" + name
        all_json["Skin"][hash(character)] = {}
        with open("Data\\Mod\\" + i, "r", encoding="utf8") as file_reader:
            lines = file_reader.readlines()
        for e in range(8):
            all_json["Skin"][hash(character)][e] = int(lines[e].strip().split("c0")[-1])

def apply_default_tweaks():
    #FIGHTER
    #Some fighter battles are incomplete and need to be fixed
    #Battle data
    for i in all_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        id = i[hash("battle_id")].value
        if id in all_json["Fighter"]:
            patch_param_entry(i, all_json["Fighter"][id], False)
            i[hash("stage_type")].value    = hash("final_stage")
            i[hash("item_table")].value    = hash("normal")
            i[hash("item_level")].value    = hash("no_item")
            i[hash("hint1_visible")].value = False
            i[hash("hint2_visible")].value = False
            i[hash("hint3_visible")].value = False
    #Enemy data
    for i in all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = i[hash("battle_id")].value
        if id in all_json["Fighter"]:
            patch_param_entry(i, all_json["Fighter"][id], False)
            i[hash("fly_rate")].value            = 1.0
            i[hash("enable_charge_final")].value = True
            i[hash("spirit_name")].value         = hash("none")
            i[hash("ability1")].value            = hash("none")
            i[hash("ability2")].value            = hash("none")
            i[hash("ability3")].value            = hash("none")
    #CUSTOM
    #Apply custom spirits
    existing_spirits = []
    for i in all_param["ui_spirit_db"][hash("db_root")]:
        id = i[hash("ui_spirit_id")].value
        if id in all_json["CustomSpirit"]:
            existing_spirits.append(id)
            patch_param_entry(i, all_json["CustomSpirit"][id], False)
            patch_text_entry("msg_spirits", "spi_" + all_json["CustomSpirit"][id]["spirit_string"], all_json["CustomSpirit"][id]["display_name"])
            change_directory_id(i[hash("directory_id")].value, all_json["CustomSpirit"][id]["spirit_slot"])
            fix_spirit_stand_pos(id, all_json["CustomSpirit"][id]["center_x"], all_json["CustomSpirit"][id]["center_y"])
            fix_spirit_effect_pos(id, hash(all_json["CustomSpirit"][id]["similar_shape"]), all_json["CustomSpirit"][id]["effect_offset_x"], all_json["CustomSpirit"][id]["effect_offset_y"])
        #Make added spirit fights rematchable and non-enhanceable
        if id in all_json["CustomBattle"]:
            i[hash("evolve_src")].value        = hash("0")
            i[hash("is_board_appear")].value   = True
            i[hash("is_rematch_target")].value = True
    #If spirit doesn't exist then create it
    for i in all_json["CustomSpirit"]:
        if not i in existing_spirits:
            add_new_spirit(i)
    #Some spirits have no real battle assigned to them so they need to be fixed
    #Battle data
    for i in all_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        id = i[hash("battle_id")].value
        if id in all_json["CustomBattle"]:
            patch_param_entry(i, all_json["CustomBattle"][id], False)
    #Enemy data
    #Add or remove enemy entries as needed
    new_list = []
    previous_id = ""
    for i in range(len(all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")])):
        current_id = all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")][i][hash("battle_id")].value
        if current_id == previous_id:
            count += 1
            if previous_id in all_json["CustomBattle"]:
                if count > len(all_json["CustomBattle"][previous_id]["enemy"]):
                    continue
        else:
            if previous_id in all_json["CustomBattle"]:
                for e in range(len(all_json["CustomBattle"][previous_id]["enemy"]) - count):
                    new_list.append(patch_param_entry(all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")][i-1].clone(), all_json["CustomBattle"][previous_id]["enemy"][count + e], True))
            count = 1
            previous_id = current_id
        if current_id in all_json["CustomBattle"]:
            new_list.append(patch_param_entry(all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")][i], all_json["CustomBattle"][current_id]["enemy"][count - 1], True))
        else:
            new_list.append(all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")][i])
    all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")].set_list(new_list)
    #TWEAK
    #Some existing spirits may need quick minor changes
    #Battle data
    for i in all_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        id = i[hash("battle_id")].value
        if id in all_json["TweakBattle"]:
            patch_param_entry(i, all_json["TweakBattle"][id], False)
    #Enemy data
    for i in all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = i[hash("battle_id")].value
        #Only allow tweaks to the main enemy
        if i[hash("entry_type")].value != hash("main_type"):
            continue
        if id in all_json["TweakBattle"]:
            patch_param_entry(i, all_json["TweakBattle"][id], False)
    #Skin
    #Adapt the skin colors used in spirit battle to the user's mods
    for i in all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = i[hash("battle_id")].value
        if i[hash("fighter_kind")].value in all_json["Skin"] and not id in all_json["Fighter"]:
            i[hash("color")].value = all_json["Skin"][i[hash("fighter_kind")].value][i[hash("color")].value]
    #MISC
    #Decrease downtime on the true final boss so that it isn't easier than the standalone versions
    for i in ["kiila", "darz"]:
        all_param["(" + i + ")duet_param"][hash("wait_time_min")][hash("value_level_min")].value = 150
        all_param["(" + i + ")duet_param"][hash("wait_time_min")][hash("value_level_max")].value = 100
        all_param["(" + i + ")duet_param"][hash("wait_time_max")][hash("value_level_min")].value = 220
        all_param["(" + i + ")duet_param"][hash("wait_time_max")][hash("value_level_max")].value = 180

def add_new_spirit(spirit):
    has_battle = spirit in all_json["CustomBattle"]
    #Append spirit entry
    #Only allow the spirit slot to either be over one of the online spirits or appended at the end
    directory_id_list = []
    for e in range(len(all_param["ui_spirit_db"][hash("db_root")])):
        directory_id_list.append(all_param["ui_spirit_db"][hash("db_root")][e][hash("directory_id")].value)
    if all_json["CustomSpirit"][spirit]["spirit_slot"] in directory_id_list or all_json["CustomSpirit"][spirit]["spirit_slot"] < 0:
        directory_id = max(max(directory_id_list), 1513) + 1
    else:
        directory_id = all_json["CustomSpirit"][spirit]["spirit_slot"]
    param_list = list(all_param["ui_spirit_db"][hash("db_root")])
    param_list.append(param_list[0].clone())
    patch_param_entry(param_list[-1], all_json["CustomSpirit"][spirit], False)
    param_list[-1][hash("ui_spirit_id")].value = spirit
    param_list[-1][hash("name_id")].value      = all_json["CustomSpirit"][spirit]["spirit_string"]
    param_list[-1][hash("save_no")].value      = directory_id - 1
    param_list[-1][hash("directory_id")].value = directory_id
    if has_battle:
        param_list[-1][hash("is_board_appear")].value   = True
        param_list[-1][hash("is_rematch_target")].value = True
    else:
        param_list[-1][hash("is_board_appear")].value   = False
        param_list[-1][hash("is_rematch_target")].value = False
    all_param["ui_spirit_db"][hash("db_root")].set_list(param_list)
    #Append layout entry
    param_list = list(all_param["ui_spirit_layout_db"][hash("db_root")])
    param_list.append(param_list[0].clone())
    param_list[-1][hash("ui_spirit_layout_id")].value = spirit
    all_param["ui_spirit_layout_db"][hash("db_root")].set_list(param_list)
    fix_spirit_stand_pos(spirit, all_json["CustomSpirit"][spirit]["center_x"], all_json["CustomSpirit"][spirit]["center_y"])
    fix_spirit_effect_pos(spirit, hash(all_json["CustomSpirit"][spirit]["similar_shape"]), all_json["CustomSpirit"][spirit]["effect_offset_x"], all_json["CustomSpirit"][spirit]["effect_offset_y"])
    #Append battle entry
    param_list = list(all_param["ui_spirits_battle_db"][hash("battle_data_tbl")])
    param_list.append(param_list[0].clone())
    if has_battle:
        patch_param_entry(param_list[-1], all_json["CustomBattle"][spirit], False)
    param_list[-1][hash("battle_id")].value = spirit
    all_param["ui_spirits_battle_db"][hash("battle_data_tbl")].set_list(param_list)
    #Append enemy entry
    param_list = list(all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")])
    if has_battle:
        for e in all_json["CustomBattle"][spirit]["enemy"]:
            param_list.append(param_list[0].clone())
            param_list[-1][hash("battle_id")].value = spirit
            patch_param_entry(param_list[-1], e, True)
    else:
        param_list.append(param_list[0].clone())
        param_list[-1][hash("battle_id")].value = spirit
    all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")].set_list(param_list)
    #Append text entry
    patch_text_entry("msg_spirits", "spi_" + all_json["CustomSpirit"][spirit]["spirit_string"], all_json["CustomSpirit"][spirit]["display_name"])

def change_directory_id(old_slot, new_slot):
    if old_slot == new_slot:
        return
    #Change slot id and shift the value for all other spirits in between
    for i in all_param["ui_spirit_db"][hash("db_root")]:
        if i[hash("directory_id")].value == old_slot:
            i[hash("directory_id")].value = new_slot
        elif new_slot < old_slot:
            if new_slot <= i[hash("directory_id")].value < old_slot:
                i[hash("directory_id")].value += 1
        elif new_slot > old_slot:
            if new_slot >= i[hash("directory_id")].value > old_slot:
                i[hash("directory_id")].value -= 1
    #Do it in the json too
    for i in all_json["CustomSpirit"]:
        if new_slot < old_slot:
            if new_slot <= all_json["CustomSpirit"][i]["spirit_slot"] < old_slot:
                all_json["CustomSpirit"][i]["spirit_slot"] += 1
        elif new_slot > old_slot:
            if new_slot >= all_json["CustomSpirit"][i]["spirit_slot"] > old_slot:
                all_json["CustomSpirit"][i]["spirit_slot"] -= 1

def fix_spirit_stand_pos(spirit, center_x, center_y):
    #Adjust the center point of a spirit image based on chosen image coordinates
    with open("Data\\Texture\\spirits_0_" + all_json["CustomSpirit"][spirit]["spirit_string"] + ".bntx", "r+b") as file:
        file.seek(0x21C)
        width = int.from_bytes(file.read(2), "little")
        file.seek(0x220)
        height = int.from_bytes(file.read(2), "little")
    for e in all_param["ui_spirit_layout_db"][hash("db_root")]:
        if e[hash("ui_spirit_layout_id")].value == spirit:
            e[hash("ui_art_on_stand_center_px_x")].value = round(width/2  - center_x)
            e[hash("ui_art_on_stand_center_px_y")].value = round(center_y - height/2)
            e[hash("ui_art_on_stand_scale")].value = 1
            e[hash("ui_art_center_px_x")].value = e[hash("ui_art_on_stand_center_px_x")].value - 5
            e[hash("ui_art_center_px_y")].value = e[hash("ui_art_on_stand_center_px_y")].value - 130
            e[hash("ui_art_scale")].value = 1
            e[hash("ui_art_type_under_center_px_x")].value = e[hash("ui_art_on_stand_center_px_x")].value
            e[hash("ui_art_type_under_center_px_y")].value = e[hash("ui_art_on_stand_center_px_y")].value - 20
            e[hash("ui_art_type_under_scale")].value = 1
            e[hash("ui_art_chara_sel_center_px_x")].value = e[hash("ui_art_on_stand_center_px_x")].value
            e[hash("ui_art_chara_sel_center_px_y")].value = e[hash("ui_art_on_stand_center_px_y")].value + 30
            e[hash("ui_art_chara_sel_scale")].value = 1
            break

def fix_spirit_effect_pos(old_layout, new_layout, offset_x, offset_y):
    #Position graphical spirit effects based on another spirit of similar shape
    data = []
    for e in all_param["ui_spirit_layout_db"][hash("db_root")]:
        if e[hash("ui_spirit_layout_id")].value == new_layout:
            effect_num = e[hash("effect_num")].value
            for o in range(15):
                data.append((e[hash("effect_pos_" + str(o) + "_x")].value, e[hash("effect_pos_" + str(o) + "_y")].value))
            break
    for e in all_param["ui_spirit_layout_db"][hash("db_root")]:
        if e[hash("ui_spirit_layout_id")].value == old_layout:
            e[hash("effect_num")].value = effect_num
            for o in range(15):
                e[hash("effect_pos_" + str(o) + "_x")].value = data[o][0] + offset_x
                e[hash("effect_pos_" + str(o) + "_y")].value = data[o][1] + offset_y
            break

def gather_data():
    #List spirits
    for i in all_param["ui_spirit_db"][hash("db_root")]:
        #Fill regular spirit list
        if (i[hash("type")].value == hash("spirits_type_attack") or i[hash("type")].value == hash("spirits_type_support")) and i[hash("is_rematch_target")].value:
            spirit_list.append(i[hash("ui_spirit_id")].value)
        #Get all summonable spirits
        if i[hash("summon_sp")].value != 0:
            summonable.append(i[hash("ui_spirit_id")].value)
        #Get all spirit indexes
        spirit_to_index[i[hash("ui_spirit_id")].value] = i[hash("save_no")].value
        #Get all spirit ranks
        spirit_to_rank[i[hash("ui_spirit_id")].value]  = i[hash("rank")].value
        #Get all spirit types
        spirit_to_type[i[hash("ui_spirit_id")].value]  = i[hash("type")].value
        #Get all spirit colors
        spirit_to_color[i[hash("ui_spirit_id")].value] = i[hash("attr")].value
    #Get all battle powers
    for i in all_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        spirit_to_power[i[hash("battle_id")].value] = i[hash("battle_power")].value
    #Finalize logic list for light maps
    for i in all_param:
        if "map_param" in i and not "dark" in i:
            for e in all_param[i][hash("map_spot_tbl")]:
                id = e[hash("spirit")].value
                if id in spirit_list:
                    check = True
                    for o in spirit_logic:
                        #Is spirit already locked ?
                        if id in spirit_logic[o]["spirit"]:
                            check = False
                            break
                        #Is spirit in an area already locked ?
                        if spirit_logic[o]["area"] in i:
                            check = False
                            spirit_logic[o]["spirit"].append(id)
                    if check:
                        spirit_logic[hash("none")]["spirit"].append(id)

def no_dlc_unlock():
    #Remove the auto unlock of DLC characters
    all_param["spirits_campaign_common_param"][hash("unlock_dlc_fighter_count")].value = 999

def rebalance_fs_meter():
    #Change the multipliers of the final smash meter to reward good performance rather than loss
    for i in all_param["spirits_battle_level_param"][hash("charge_final_param")]:
        i[hash("by_time_mul")].value   = 0
        i[hash("by_attack_mul")].value = 5
        i[hash("damage_mul")].value    = 0

def remove_dlc(fighter):
    #Remove DLC fighter
    fighter_skins = []
    found = False
    for i in all_json["Fighter"]:
        if i == hash(fighter):
            fighter_skins.append(i)
            found = True
        elif found:
            if all_json["Fighter"][i]["main_entry"]:
                break
            fighter_skins.append(i)
    for i in fighter_skins:
        del all_json["Fighter"][i]
    #Remove DLC spirit
    if hash(fighter) in fighter_to_dlc:
        for i in fighter_to_dlc[hash(fighter)]:
            if i in spirit_list:
                spirit_list.remove(i)

def randomize_spirit(fighter, spirit, master, boss):
    #Fighter
    fighter_dict = create_fighter_dict()
    values = list(fighter_dict.values())
    random.shuffle(values)
    fighter_replacement = dict(zip(fighter_dict, values))
    #Spirit
    values = list(spirit_list)
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
    for i in all_replacement:
        all_replacement_invert[all_replacement[i]] = i

def create_fighter_dict():
    #Pick one skin to use per fighter
    old_fighter_pool = []
    new_fighter_pool = []
    fighter_alt      = []
    for i in all_json["Fighter"]:
        if all_json["Fighter"][i]["main_entry"]:
            old_fighter_pool.append(i)
            if fighter_alt:
                new_fighter_pool.append(random.choice(fighter_alt))
            fighter_alt = [i]
        else:
            fighter_alt.append(i)
    #Do it one more time for the end of the file
    new_fighter_pool.append(random.choice(fighter_alt))
    return dict(zip(old_fighter_pool, new_fighter_pool))

def randomize_mii_specials():
    for i in all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = i[hash("battle_id")].value
        if id in [hash("mii_brawler_ssb"), hash("mii_swordfighter_ssb"), hash("mii_gunner_ssb")]:
            for e in ["n", "s", "hi", "lw"]:
                i[hash("mii_sp_" + e)].value = random.randint(0, 2)

def patch_boss_entities():
    #Update sub boss placement
    for i in all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        value = i[hash("fighter_kind")].value
        if value in boss_to_properties:
            i[hash("fighter_kind")].value = all_replacement[value]
    #Change Giga Bowser's stage to a standard walkoff as most bosses don't work on Final Destination
    #The best fit for this would be the result stage
    all_param["ui_spirits_battle_db"][hash("battle_data_tbl")][1484][hash("ui_stage_id")].value              = hash("ui_stage_result_stage")
    all_param["ui_spirits_battle_db"][hash("battle_data_tbl")][1484][hash("stage_additional_setting")].value = 0
    #This stage ID does not exist in vanilla so it needs to be created
    stage_list = list(all_param["ui_stage_db"][hash("db_root")])
    stage_list.append(stage_list[111].clone())
    stage_list[-1][hash("ui_stage_id")].value           = hash("ui_stage_result_stage")
    stage_list[-1][hash("name_id")].value               = "ResultStage"
    stage_list[-1][hash("stage_place_id")].value        = hash("resultstage")
    stage_list[-1][hash("secret_stage_place_id")].value = hash("resultstage")
    all_param["ui_stage_db"][hash("db_root")].set_list(stage_list)
    #Increase Giga Bowser's size to make up for the bigger stage
    all_param["fighter_param"][hash("fighter_param_table")][90][hash("scale")].value *= 1.5
    all_param["vl"][hash("param_special_n")][0][hash("fire_scale_min")].value        *= 1.5
    all_param["vl"][hash("param_special_n")][0][hash("fire_scale_max")].value        *= 1.5

def randomize_skill():
    #Get all skill data as tuples
    data = []
    for i in all_param["ui_campaign_skill_db"][hash("db_root")]:
        if i[hash("spirits_ability_id")].value != hash("none"):
            data.append((
                i[hash("node_index")].value      ,
                i[hash("connection0")].value     ,
                i[hash("connection1")].value     ,
                i[hash("connection2")].value     ,
                i[hash("connection3")].value     ,
                i[hash("connection4")].value     ,
                i[hash("connection_count")].value
            ))
    #Reassign data at random
    for i in all_param["ui_campaign_skill_db"][hash("db_root")]:
        if i[hash("spirits_ability_id")].value != hash("none"):
            chosen = any_pick(data)
            i[hash("node_index")].value       = chosen[0]
            i[hash("connection0")].value      = chosen[1]
            i[hash("connection1")].value      = chosen[2]
            i[hash("connection2")].value      = chosen[3]
            i[hash("connection3")].value      = chosen[4]
            i[hash("connection4")].value      = chosen[5]
            i[hash("connection_count")].value = chosen[6]

def rebalance_spirit(boss):
    #SPIRIT
    for i in all_param["ui_spirit_db"][hash("db_root")]:
        #Check ID and evolve from
        id     = i[hash("ui_spirit_id")].value
        origin = i[hash("evolve_src")].value
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
            if star_num  < 1:
                star_num = 1
            if star_num  > 4:
                star_num = 4
        #Change rank
        i[hash("rank")].value = rank_to_star_invert[star_num]
        #Base fighter and master spirits on battle power
        if id in all_json["Fighter"] or id in master_to_properties:
            multiplier = spirit_to_power[all_replacement_invert[id]]/spirit_to_power[id]
        #Base regular spirits on rank
        else:
            multiplier = rank_to_intensity[i[hash("rank")].value]/rank_to_intensity[spirit_to_rank[id]]
        #Multiply spirit stats
        if i[hash("type")].value         == hash("spirits_type_attack"):
            i[hash("base_attack")].value  = round(i[hash("base_attack")].value  * multiplier ** 0.6)
            i[hash("max_attack")].value   = round(i[hash("max_attack")].value   * multiplier ** 0.6)
            i[hash("base_defense")].value = round(i[hash("base_defense")].value * multiplier ** 0.6)
            i[hash("max_defense")].value  = round(i[hash("max_defense")].value  * multiplier ** 0.6)
        #Make sure stats don't exceed the max
        if i[hash("max_attack")].value   > 10000:
            i[hash("max_attack")].value  = 10000
        if i[hash("max_defense")].value  > 10000:
            i[hash("max_defense")].value = 10000
        #Other properties
        i[hash("reward_capacity")].value = round(i[hash("reward_capacity")].value * multiplier ** 1.25)
        i[hash("exp_lv_max")].value      = round(i[hash("exp_lv_max")].value      * multiplier ** 0.88)
        i[hash("battle_exp")].value      = round(i[hash("battle_exp")].value      * multiplier ** 0.5)
        i[hash("shop_price")].value      = round(i[hash("shop_price")].value      * multiplier ** 1.8)
        #Make stats multiples of specific numbers                                                                     
        i[hash("exp_lv_max")].value = round(i[hash("exp_lv_max")].value/5)  *5
        i[hash("battle_exp")].value = round(i[hash("battle_exp")].value/50) *50
        i[hash("shop_price")].value = round(i[hash("shop_price")].value/500)*500
        #Get fallback battle ID in case there is one
        if i[hash("replace_battle_id")].value != hash(""):
            spirit_override[i[hash("replace_battle_id")].value] = id
    #BATTLE
    for i in all_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        #Check ID with potential override
        if i[hash("battle_id")].value in spirit_override:
            id = spirit_override[i[hash("battle_id")].value]
        else:
            id = i[hash("battle_id")].value
        #Skip if not randomized
        if not id in all_replacement_invert:
            continue
        #Base fighter and master spirits on battle power
        if id in all_json["Fighter"] or id in master_to_properties:
            multiplier = spirit_to_power[all_replacement_invert[id]]/spirit_to_power[id]
        #Base regular spirit on rank
        else:
            multiplier = rank_to_intensity[spirit_to_rank[all_replacement_invert[id]]]/rank_to_intensity[spirit_to_rank[id]]
        #Multiply battle stats
        i[hash("battle_power")].value = round(i[hash("battle_power")].value * multiplier ** 1.0)
        #Make stats multiples of specific numbers
        i[hash("battle_power")].value = round(i[hash("battle_power")].value/100)*100
    #FIGHTER
    for i in all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        #Check ID with potential override
        if i[hash("battle_id")].value in spirit_override:
            id = spirit_override[i[hash("battle_id")].value]
        else:
            id = i[hash("battle_id")].value
        #Skip if not randomized
        if not id in all_replacement_invert:
            continue
        #Base fighter and master spirits on battle power
        if id in all_json["Fighter"] or id in master_to_properties:
            multiplier = spirit_to_power[all_replacement_invert[id]]/spirit_to_power[id]
        #Base regular spirit on rank
        else:
            multiplier = rank_to_intensity[spirit_to_rank[all_replacement_invert[id]]]/rank_to_intensity[spirit_to_rank[id]]
        #Multiply enemy stats
        attack      = round(i[hash("attack")].value  * multiplier ** 1.0)
        defense     = round(i[hash("defense")].value * multiplier ** 1.2)
        cpu_lv      = round(i[hash("cpu_lv")].value  * multiplier ** 0.56)
        #Make stats multiples of specific numbers
        attack      = round(attack/50) *50
        defense     = round(defense/50)*50
        #Make sure stats don't exceed the max
        if attack   > 10000:
            attack  = 10000
        if defense  > 10000:
            defense = 10000
        if cpu_lv   > 100:
            cpu_lv  = 100
        #Patch values
        i[hash("attack")].value  = attack
        i[hash("defense")].value = defense
        i[hash("cpu_lv")].value  = cpu_lv

def shorten_playthrough(length):
    #Create shorter playthroughs by removing spirit spots at random
    irrelevent = [
        hash(""),
        hash("spot_blind_flag_002"),
        hash("spot_blind_flag_013"),
        hash("spot_blind_flag_004"),
        hash("spot_blind_flag_020")
    ]
    hand_trigger = [
        hash(0x0fc90556e2),
        hash(0x0fdbb0f90c),
        hash(0x18db4ecfa3),
        hash(0x18c9fb604d),
        hash(0x18542c58f4),
        hash("cannon_rot_motion_rate_2"),
        hash(0x1871470728)
    ]
    remove_list = []
    keep_list   = []
    for i in all_param:
        if "map_param" in i:
            important   = []
            tutorial    = []
            hand_event  = []
            if i == "spirits_campaign_map_param_light":
                #One spot to uncover all clouds
                important.append(hash("sp01_02"))
                for e in all_param[i][hash("map_blind_tbl")]:
                    e[hash("chain_spot_01")].value = hash("sp01_02")
                    for o in range(9):
                        e[hash("chain_spot_" + "{:02d}".format(o + 2))].value = hash("")
                #Button prompt tutorials
                tutorial.append(hash("sp01_01"))
                tutorial.append(hash("fig01_01"))
                tutorial.append(hash("fig01_02"))
                tutorial.append(hash("fig01_03"))
                tutorial.append(hash("fig01_04"))
                #Hand events
                hand_event.append(hash("spot_masterhand_flag"))
                hand_event.append(hash("spot_masterhand_l_flag"))
                hand_event.append(hash("spot_masterhand_r_flag"))
            if i == "spirits_campaign_map_param_dark":
                #One spot to uncover all top clouds
                important.append(hash("sp52_01"))
                for e in range(7):
                    all_param[i][hash("map_blind_tbl")][e][hash("chain_spot_01")].value = hash("sp52_01")
                    for o in range(9):
                        all_param[i][hash("map_blind_tbl")][e][hash("chain_spot_" + "{:02d}".format(o + 2))].value = hash("")
                #One spot to uncover all left clouds
                important.append(hash("sp53_01"))
                for e in range(5):
                    all_param[i][hash("map_blind_tbl")][e + 7][hash("chain_spot_01")].value = hash("sp53_01")
                    for o in range(9):
                        all_param[i][hash("map_blind_tbl")][e + 7][hash("chain_spot_" + "{:02d}".format(o + 2))].value = hash("")
                #One spot to uncover all right clouds
                important.append(hash("sp_54_01"))
                for e in range(5):
                    all_param[i][hash("map_blind_tbl")][e + 7 + 5][hash("chain_spot_01")].value = hash("sp_54_01")
                    for o in range(9):
                        all_param[i][hash("map_blind_tbl")][e + 7 + 5][hash("chain_spot_" + "{:02d}".format(o + 2))].value = hash("")
                #Hand events
                hand_event.append(hash("spot_crazy_pos_flag_01"))
                hand_event.append(hash("spot_crazy_pos_flag_02"))
                hand_event.append(hash("spot_boss_crazy_pos_02"))
                hand_event.append(hash("spot_crazy_pos_flag_03"))
                hand_event.append(hash("spot_crazy_pos_flag_04"))
                hand_event.append(hash("spot_crazy_pos_flag_05"))
            #Remove spirits spots for shorter length
            for e in all_param[i][hash("map_spot_tbl")]:
                id = e[hash("spirit")].value
                remove = False
                #Determine if the spirit must be removed
                if id in keep_list:
                    pass
                elif id in remove_list:
                    remove = True
                elif random.randint(1, 5) <= length:
                    pass
                elif e[hash("hash")].value in important:
                    pass
                elif id in all_json["Fighter"] or id in spirit_list or id in master_to_properties:
                    remove = True
                #Proceed
                if remove:
                    #Remove spirit from logic
                    for o in spirit_logic:
                        if id in spirit_logic[o]["spirit"]:
                            spirit_logic[o]["spirit"].remove(id)
                    #Remove spirit from map
                    e[hash("type")].value = hash("spot_type_space")
                    #Keep a random food item if the spirit spawns from event
                    if e[hash(0x1849e18674)].value in irrelevent:
                        e[hash("sub_type")].value = hash("")
                    else:
                        e[hash("sub_type")].value = hash(random.choice(food_type))
                    #Disable the last map event
                    if e[hash("act_hash_clear")].value == hash(0x1838832598):
                        e[hash("act_hash_clear")].value = hash("")
                    #Remove the button promptfor the few tutorial spots
                    if e[hash("hash")].value in tutorial:
                        e[hash("act_hash_decide")].value = hash("")
                    #Remove corresponding master activity too
                    if id in master_to_properties:
                        for o in master_to_properties[id][1]:
                            all_param[i][hash("map_spot_tbl")][o][hash("sub_type")].value = hash("")
                    #Keep spirit status in memory
                    remove_list.append(id)
                else:
                    keep_list.append(id)
            #Remove most hand fights
            #Doesn't work
            #Some spots block you despite doing the necessary changes
            #    if e[hash(0x1849e18674)].value in hand_event:
            #        e[hash("type")].value            = hash("spot_type_space")
            #        e[hash("sub_type")].value        = hash("")
            #        e[hash(0x133f92093f)].value      = hash("")
            #        e[hash(0x13a69b5885)].value      = hash("")
            #        e[hash(0x13d19c6813)].value      = hash("")
            #        e[hash(0x1849e18674)].value      = hash("")
            #        e[hash(0x18d0e8d7ce)].value      = hash("")
            #        e[hash("act_hash_arrive")].value = hash("")
            #        e[hash("act_hash_decide")].value = hash("")
            #        e[hash("act_hash_clear")].value  = hash("")
            #    if e[hash("act_hash_clear")].value in hand_trigger:
            #        e[hash("act_hash_clear")].value  = hash("")
            #for e in all_param[i][hash("map_route_tbl")]:
            #    if e[hash(0x1849e18674)].value in hand_event:
            #        e[hash(0x1849e18674)].value      = hash("")

def patch_spot():
    #Apply shuffled changes to all spirit spots
    for i in all_param:
        if "map_param" in i:
            for e in all_param[i][hash("map_spot_tbl")]:
                id = e[hash("spirit")].value
                #Change spirit
                if id in all_replacement:
                    e[hash("spirit")].value    = all_replacement[id]
                    e[hash("battle_id")].value = hash("-1")
                    e[hash("item")].value      = hash("")
                    #Change the corresponding activity spots for master spirits
                    if e[hash("type")].value == hash("spot_type_build"):
                        e[hash("sub_type")].value = master_to_properties[all_replacement[id]][0]
                        for o in master_to_properties[id][1]:
                            all_param[i][hash("map_spot_tbl")][o][hash("sub_type")].value = master_to_properties[all_replacement[id]][2]
                #Change the corresponding rewards for boss characters
                if id in boss_to_properties_invert:
                    if boss_to_properties_invert[id] in all_replacement:
                        #Battle ID must remain the same
                        if e[hash("battle_id")].value == hash("-1"):
                            e[hash("battle_id")].value = id
                        e[hash("spirit")].value = boss_to_properties[all_replacement[boss_to_properties_invert[id]]][0]
                        e[hash("item")].value   = boss_to_properties[all_replacement[boss_to_properties_invert[id]]][1]

def patch_requirement():
    #Determine logic behind key spirits
    barrier = list(spirit_logic)
    barrier.remove(hash("none"))
    random.shuffle(barrier)
    for i in barrier:
        spirit_logic[i]["key"] = any_pick(spirit_logic[hash("none")]["spirit"])
        #Checking if barrier is locked behind another barrier
        if spirit_logic[spirit_logic[i]["lock"]]["spirit"]:
            lock = spirit_logic[i]["lock"]
        else:
            lock = hash("none")
        spirit_logic[lock]["spirit"].extend(spirit_logic[i]["spirit"])
        spirit_logic[lock]["spirit"] = list(dict.fromkeys(spirit_logic[lock]["spirit"]))
        spirit_logic[i]["spirit"].clear()
    #Change blockade spirit requirements to reflect the logic
    for i in all_param["spirits_campaign_barrier_param"][hash("barrier_tbl")]:
        id = i[hash("spirit_01")].value
        if id == hash(""):
            continue
        i[hash("spirit_01")].value = all_replacement[spirit_logic[id]["key"]]
        for e in range(9):
            i[hash("spirit_" + "{:02d}".format(e + 2))].value = hash("")

def patch_reward():
    #Change spirits that are found directly in chests
    for i in all_param["spirits_campaign_item_param"][hash("item_tbl")]:
        id = i[hash("key")].value
        if id in all_replacement:
            i[hash("key")].value = all_replacement[id]

def patch_shop():
    #Change spirits that are sold at the shops
    for i in range(5):
        for e in all_param["ui_shop_db"][hash("shop_spirit_adv_" + str(i + 1))]:
            id = e[hash("ui_spirit_id")].value
            if id in all_replacement:
                e[hash("ui_spirit_id")].value = all_replacement[id]

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
    for i in all_param["ui_spirit_db"][hash("db_root")]:
        id = i[hash("ui_spirit_id")].value
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
            for e in range(5):
                if e < item_num - common_num:
                    i[hash("summon_item" + str(e + 1))].value          = random.choice(spirit_list)
                    i[hash("summon_item" + str(e + 1) + "_num")].value = 1
                elif e < item_num:
                    i[hash("summon_item" + str(e + 1))].value          = random.choice(common_list)
                    i[hash("summon_item" + str(e + 1) + "_num")].value = random.choice(common_quantity_list)
                else:
                    i[hash("summon_item" + str(e + 1))].value          = hash("none")
                    i[hash("summon_item" + str(e + 1) + "_num")].value = 0
        else:
            #Make the rest non-summonable
            for e in range(5):
                i[hash("summon_item" + str(e + 1))].value          = hash("none")
                i[hash("summon_item" + str(e + 1) + "_num")].value = 0

def patch_master_element():
    #Change master spirit spot elements based on their new location
    for i in all_param["spirits_campaign_resource_param"][hash(0x11a29ee536)]:
        id = i[hash("type_sub")].value
        if id in master_to_properties_invert:
            element = master_to_properties[all_replacement_invert[master_to_properties_invert[id]]][3]
            i[hash("obj_model_resource_name")].value       = hash("point_spirit_" + element + "_on")
            i[hash("obj_model_resource_name_clear")].value = hash("point_spirit_" + element + "_off")
            i[hash("obj_effect_hash")].value               = hash("cp_map_" + element + "spirits")
            i[hash("obj_effect_hash_out")].value           = hash("cp_map_" + element + "spirits_release")
    #This however does not affect the intro animations, maybe those are hardcoded

def patch_param_entry(entry, data, special):
    for i in data:
        try:
            if isinstance(data[i], str):
                entry[hash(i)].value = hash(data[i])
            else:
                entry[hash(i)].value = data[i]
        except IndexError:
            continue
    if special:
        if data["use_spirit"]:
            entry[hash("spirit_name")].value = entry[hash("battle_id")].value
        else:
            entry[hash("spirit_name")].value = hash("none")
    return entry

def patch_text_entry(file, entry, text):
    #Create msbt patches directly when changing a string entry
    try:
        test = all_text[file]
    except KeyError:
        all_text[file] = ET.Element("xmsbt")
    entry = ET.SubElement(all_text[file], "entry", label=entry)
    ET.SubElement(entry, "text").text = text

def copy_spirit_images(path):
    #Copy spirit UIs to mod folder
    spirit_images = []
    for i in os.listdir("Data\\Texture"):
        name, extension = os.path.splitext(i)
        spirit_images.append(name.replace("spirits_0_", "").replace("spirits_1_", "").replace("spirits_2_", ""))
    spirit_images = list(dict.fromkeys(spirit_images))
    for i in spirit_images:
        for e in range(3):
            shutil.copyfile("Data\\Texture\\spirits_" + str(e) + "_" + i + ".bntx", path + "\\ui\\replace\\spirits\\spirits_" + str(e) + "\\spirits_" + str(e) + "_" + i + ".bntx")
    #To make outlines:
    #Image dimensions x0.55
    #Content dimensions x0.9
    #Drop shadow grow radius 1
    #Gaussian blur 1.25

def save_param(path):
    for i in all_param:
        all_param[i].save(path + "\\" + all_json["FileToPath"][i] + "\\" + i.split(")")[-1] + ".prc")

def convert_param_to_patch(path):
    for i in all_param:
        vanilla_file = "Data\\Param\\" + i + ".prc"
        modded_file = path + "\\" + all_json["FileToPath"][i] + "\\" + i.split(")")[-1] + ".prc"
        os.system("cmd /c parcel diff \"" + vanilla_file + "\" \"" + modded_file + "\" \"" + modded_file + "x\"")
        os.remove(modded_file)

def save_text(path):
    for i in all_text:
        tree = minidom.parseString(ET.tostring(all_text[i])).toprettyxml(encoding="utf-16", indent="	")
        with open(path + "\\ui\\message\\" + i + ".xmsbt", "wb") as filewriter:
            filewriter.write(tree)

def get_spirits_in_wol():
    #Get a list of the spirits that can be obtained through WoL
    list = []
    #Map spirits
    for i in all_param:
        if "map_param" in i:
            for e in all_param[i][hash("map_spot_tbl")]:
                if e[hash("type")].value == hash("spot_type_spirit"):
                    list.append(e[hash("spirit")].value)
    #Chest spirits
    for i in all_param["spirits_campaign_item_param"][hash("item_tbl")]:
        id = i[hash("key")].value
        if id in spirit_list:
            list.append(id)
    #Summonable spirits
    for i in all_param["ui_spirit_db"][hash("db_root")]:
        if i[hash("summon_item1")].value != hash("none"):
            list.append(i[hash("ui_spirit_id")].value)
    #Shop spirits
    for i in range(5):
        for e in all_param["ui_shop_db"][hash("shop_spirit_adv_" + str(i + 1))]:
            id = e[hash("ui_spirit_id")].value
            if id in spirit_list:
                list.append(id)
    return list

def reset_spirit(path):
    with open(path, "r+b") as file:
        #Spirits
        file.seek(0x43471C)
        for i in range(6000):
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
        for i in range(2000):
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
    spirit_pool = list(spirit_list)
    #One primary of each color
    for i in ["atk", "def", "trw"]:
        chosen = random.choice(spirit_pool)
        while get_current_rank(chosen) != hash("hope") or spirit_to_color[chosen] != hash("spirits_attr_" + i) or chosen in spirit_in_wol:
            chosen = random.choice(spirit_pool)
        spirit_pool.remove(chosen)
        start_spirits.append(chosen)
    #Three supports
    for i in range(3):
        chosen = random.choice(spirit_pool)
        while get_current_rank(chosen) != hash("hope") or spirit_to_type[chosen] != hash("spirits_type_support") or chosen in spirit_in_wol:
            chosen = random.choice(spirit_pool)
        spirit_pool.remove(chosen)
        start_spirits.append(chosen)
    #Open save
    with open(path, "r+b") as file:
        #Put spirits in inventory
        file.seek(0x43471C)
        for i in range(len(start_spirits)):
            file.write((i).to_bytes(4, "little"))
            file.write((0).to_bytes(6, "little"))
            file.write(spirit_to_index[start_spirits[i]].to_bytes(2, "little"))
            file.write((0).to_bytes(4, "little"))
            file.write((0xFF0E).to_bytes(2, "little"))
            file.write((0).to_bytes(34, "little"))
        #Unlock them in collection
        for i in range(len(start_spirits)):
            file.seek(0x426C5C + spirit_to_index[start_spirits[i]]*0x1C + 0x1A)
            file.write((0x0D).to_bytes(1, "little"))

def get_current_rank(spirit):
    try:
        return spirit_to_rank[all_replacement_invert[spirit]]
    except KeyError:
        return spirit_to_rank[spirit]

def any_pick(array):
    #Pick-and-remove function
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
    for i in all_param["ui_spirit_db"][hash("db_root")]:
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
    for i in all_param["ui_spirits_battle_db"][hash("battle_data_tbl")]:
        id = i[hash("battle_id")].value
        if id in spirit_list and spirit_to_rank[id] == hash(rank):
            count += 1
            battle_power += i[hash("battle_power")].value
    battle_power /= count
    
    count = 0
    attack = 0
    defense = 0
    cpu_lv = 0
    for i in all_param["ui_spirits_battle_db"][hash("fighter_data_tbl")]:
        id = i[hash("battle_id")].value
        if id in spirit_list and spirit_to_rank[id] == hash(rank):
            count += 1
            attack += i[hash("attack")].value
            defense += i[hash("defense")].value
            cpu_lv += i[hash("cpu_lv")].value
    attack /= count
    defense /= count
    cpu_lv /= count
    
    print("max_attack " + str(max_attack))
    print("max_defense " + str(max_defense))
    print("reward_capacity " + str(reward_capacity))
    print("exp_lv_max " + str(exp_lv_max))
    print("battle_exp " + str(battle_exp))
    print("shop_price " + str(shop_price))
    print("battle_power " + str(battle_power))
    print("attack " + str(attack))
    print("defense " + str(defense))
    print("cpu_lv " + str(cpu_lv))