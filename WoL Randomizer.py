import Manager

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import json
import traceback
import configparser
import sys
import random
import math
import re
import os
import shutil
import requests
import zipfile
import subprocess

#Get script name

script_name = os.path.splitext(os.path.basename(__file__))[0]

#Config

config = configparser.ConfigParser()
config.optionxform = str
config.read("Data\\config.ini")

#Functions

def writing():
    with open("Data\\config.ini", "w") as file_writer:
        config.write(file_writer)
    sys.exit()

#Threads

class Signaller(QObject):
    progress = Signal(int)
    finished = Signal()
    error    = Signal()

class Generate(QThread):
    def __init__(self, seed, backup):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.seed = seed
        self.backup = backup
    
    def run(self):
        try:
            self.process()
        except Exception:
            self.signaller.error.emit()
            raise

    def process(self):
        self.signaller.progress.emit(0)
        
        #Initialize
        
        Manager.init()
        Manager.load_param()
        Manager.load_text()
        Manager.load_json()
        
        #Get mod directory
        
        if config.getboolean("Platform", "bSwitch") and config.get("Misc", "sModFolder"):
            mod_dir = config.get("Misc", "sModFolder")     + f"\\{script_name}"
        elif config.getboolean("Platform", "bRyujinx") and config.get("Misc", "sRyujinxFolder"):
            mod_dir = config.get("Misc", "sRyujinxFolder") + f"\\sdcard\\ultimate\\mods\\{script_name}"
        else:
            mod_dir = script_name
        
        #Reset mod directory
        
        if os.path.isdir(mod_dir):
            shutil.rmtree(mod_dir)
        
        #Initialize mod directory
        
        for directory in list(Manager.mod_data["FileToPath"].values()):
            if not os.path.isdir(f"{mod_dir}\\{directory}"):
                os.makedirs(f"{mod_dir}\\{directory}")
        if not os.path.isdir(f"{mod_dir}\\ui\\message"):
            os.makedirs(f"{mod_dir}\\ui\\message")
        for index in range(3):
            if not os.path.isdir(f"{mod_dir}\\ui\\replace\\spirits\\spirits_{index}"):
                os.makedirs(f"{mod_dir}\\ui\\replace\\spirits\\spirits_{index}")
            if Manager.use_event_data and not os.path.isdir(f"{mod_dir}\\ui\\replace_patch\\spirits\\spirits_{index}"):
                os.makedirs(f"{mod_dir}\\ui\\replace_patch\\spirits\\spirits_{index}")
        
        #ApplyTweaks
        
        Manager.apply_default_tweaks()
        Manager.gather_data()
        
        if config.getboolean("Extra", "bRebalanceFSM"):
            Manager.rebalance_fs_meter()
        if config.getboolean("Extra", "bNoAutoDLC"):
            Manager.no_dlc_unlock()
        if config.getboolean("Extra", "bShortTrueEnd"):
            Manager.shorten_final_boss()
        if config.getboolean("Extra", "bNerfSnacks"):
            Manager.nerf_snacks()
        
        #Check DLCs
        
        if config.getboolean("DLC", "bPackun"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("piranha_plant")
        else:
            Manager.remove_dlc("piranha_plant")
        if config.getboolean("DLC", "bJack"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("jack_phantom_thief")
        else:
            Manager.remove_dlc("jack_phantom_thief")
        if config.getboolean("DLC", "bBrave"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("brave_11")
        else:
            Manager.remove_dlc("brave_11")
        if config.getboolean("DLC", "bBuddy"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("buddy")
        else:
            Manager.remove_dlc("buddy")
        if config.getboolean("DLC", "bDolly"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("dolly")
        else:
            Manager.remove_dlc("dolly")
        if config.getboolean("DLC", "bMaster"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("master_1")
        else:
            Manager.remove_dlc("master_1")
        if config.getboolean("DLC", "bTantan"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("tantan_minmin")
        else:
            Manager.remove_dlc("tantan_minmin")
        if config.getboolean("DLC", "bPickel"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("pickel_steve")
        else:
            Manager.remove_dlc("pickel_steve")
        if config.getboolean("DLC", "bEdge"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("edge_sephiroth")
        else:
            Manager.remove_dlc("edge_sephiroth")
        if config.getboolean("DLC", "bElement"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("element_homura")
        else:
            Manager.remove_dlc("element_homura")
        if config.getboolean("DLC", "bDemon"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("demon_kazuya_mishima_00")
        else:
            Manager.remove_dlc("demon_kazuya_mishima_00")
        if config.getboolean("DLC", "bTrail"):
            if config.getboolean("Extra", "bNoAutoDLC"):
                Manager.add_dlc_to_map("trail_sora")
        else:
            Manager.remove_dlc("trail_sora")
        
        #Randomize
        
        random.seed(self.seed)
        Manager.randomize_spirit(
            config.getboolean("Randomize", "bFighterSpirit"),
            config.getboolean("Randomize", "bSpiritSpirit"),
            config.getboolean("Randomize", "bMasterSpirit"),
            config.getboolean("Randomize", "bBossEntity")
        )
        
        if config.getboolean("Randomize", "bFighterSpirit"):
            random.seed(self.seed)
            Manager.randomize_mii_specials()
        
        if config.getboolean("Randomize", "bChestReward"):
            random.seed(self.seed)
            Manager.randomize_rewards()
        
        if config.getboolean("Randomize", "bBossGimmick"):
            random.seed(self.seed)
            Manager.randomize_boss_gimmicks()
        
        if config.getboolean("Randomize", "bSkillTree"):
            random.seed(self.seed)
            Manager.randomize_skill()
        
        Manager.rebalance_spirit(config.getboolean("Randomize", "bBossEntity"))
        
        if config.getint("Length", "iValue") < 5:
            random.seed(self.seed)
            Manager.shorten_playthrough(config.getint("Length", "iValue"))
        
        if config.getboolean("Randomize", "bFighterSpirit") or config.getboolean("Randomize", "bSpiritSpirit") or config.getboolean("Randomize", "bMasterSpirit") or config.getboolean("Randomize", "bBossEntity"):
            Manager.patch_spot()
        
        if config.getboolean("Randomize", "bSpiritSpirit") or config.getint("Length", "iValue") < 5:
            random.seed(self.seed)
            Manager.patch_requirement(config.getboolean("Randomize", "bSpiritSpirit"))
        
        if config.getboolean("Randomize", "bSpiritSpirit"):
            random.seed(self.seed)
            Manager.patch_reward()
            Manager.patch_shop()
            Manager.patch_summon()
        
        if config.getboolean("Randomize", "bMasterSpirit"):
            Manager.patch_master_element()
        
        if config.getboolean("Randomize", "bBossEntity"):
            Manager.patch_boss_entities()
        
        Manager.patch_text_entry("msg_campaign", "cam_save_level_sele", str(self.seed))
        Manager.patch_text_entry("msg_campaign", "cam_save_num_area",   str(self.seed))
        
        #Mod files
        
        Manager.save_param(mod_dir)
        Manager.save_floor(mod_dir)
        Manager.save_text(mod_dir)
        Manager.save_texture(mod_dir)
        if config.getboolean("Output", "bPatch"):
            Manager.convert_param_to_patch(mod_dir)
        
        #Save files
        
        if config.getboolean("Extra", "bResetSpirit"):
            
            #Switch
            if config.getboolean("Platform", "bSwitch"):
                    
                #Backup save file
                if self.backup:
                    if not os.path.isdir("Backup"):
                        os.makedirs("Backup")
                    shutil.copyfile(config.get("Misc", "sSaveFile"), "Backup\\system_data.bin")
                
                #Modify save file
                Manager.reset_spirit(config.get("Misc", "sSaveFile"))
                if config.getboolean("Extra", "bStartSpirit"):
                    random.seed(self.seed)
                    Manager.start_spirit(config.get("Misc", "sSaveFile"))
            
            #Ryujinx
            elif config.getboolean("Platform", "bRyujinx"):
                    
                #The save directory name can differ between users
                half_path = config.get("Misc", "sRyujinxFolder") + "\\bis\\user\\save"
                for directory in os.listdir(half_path):
                    full_path_0 = f"{half_path}\\{directory}\\0\\save_data\\system_data.bin"
                    full_path_1 = f"{half_path}\\{directory}\\1\\save_data\\system_data.bin"
                    if os.path.isfile(full_path_0):
                
                        #Backup save file
                        if self.backup:
                            if not os.path.isdir("Backup"):
                                os.makedirs("Backup")
                            shutil.copyfile(full_path_0, f"Backup\\{directory}\\system_data.bin")
                        
                        #Modify save file
                        Manager.reset_spirit(full_path_0)
                        Manager.reset_spirit(full_path_1)
                        if config.getboolean("Extra", "bStartSpirit"):
                            random.seed(self.seed)
                            Manager.start_spirit(full_path_0)
                            Manager.start_spirit(full_path_1)
        
        self.signaller.progress.emit(1)
        self.signaller.finished.emit()

class Update(QThread):
    def __init__(self, progress_bar, api):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.progress_bar = progress_bar
        self.api = api
    
    def run(self):
        try:
            self.process()
        except Exception:
            self.signaller.error.emit()
            raise

    def process(self):
        progress = 0
        zip_name = "WoL Randomizer.zip"
        exe_name = script_name + ".exe"
        self.signaller.progress.emit(progress)
        
        #Download
        
        with open(zip_name, "wb") as file_writer:
            url = requests.get(self.api["assets"][0]["browser_download_url"], stream=True)
            for data in url.iter_content(chunk_size=4096):
                file_writer.write(data)
                progress += len(data)
                self.signaller.progress.emit(progress)
        
        self.progress_bar.setLabelText("Extracting...")
        
        #Reset folders
        
        shutil.rmtree("Data\\Event")
        shutil.rmtree("Data\\Floor")
        shutil.rmtree("Data\\Param")
        os.remove("Data\\background.png")
        os.remove("Data\\browse.png")
        os.remove("Data\\config.ini")
        os.remove("Data\\icon.png")
        
        os.rename(exe_name, "delete.me")
        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            zip_ref.extractall("")
        os.remove(zip_name)
        
        #Carry previous config settings
        
        new_config = configparser.ConfigParser()
        new_config.optionxform = str
        new_config.read("Data\\config.ini")
        for each_section in new_config.sections():
            for (each_key, each_val) in new_config.items(each_section):
                if each_key == "sVersion":
                    continue
                try:
                    new_config.set(each_section, each_key, config.get(each_section, each_key))
                except (configparser.NoSectionError, configparser.NoOptionError):
                    continue
        with open("Data\\config.ini", "w") as file_writer:
            new_config.write(file_writer)
        
        #Open new EXE
        
        subprocess.Popen(exe_name)
        self.signaller.finished.emit()

#Interface

class QCheckBox(QCheckBox):
    def nextCheckState(self):
        if self.checkState() == Qt.Unchecked:
            self.setCheckState(Qt.PartiallyChecked)
        elif self.checkState() == Qt.PartiallyChecked:
            self.setCheckState(Qt.Unchecked)
    
    def checkStateSet(self):
        super().checkStateSet()
        if self.checkState() == Qt.Checked:
            self.setCheckState(Qt.PartiallyChecked)

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setEnabled(False)
        self.initUI()
        self.check_for_updates()

    def initUI(self):
        self.setStyleSheet("QWidget{background:transparent; color: #ffffff; font-family: Cambria; font-size: 18px}"
        + "QMessageBox{background-color: #1d1d1d}"
        + "QDialog{background-color: #1d1d1d}"
        + "QProgressDialog{background-color: #1d1d1d}"
        + "QPushButton{background-color: #1d1d1d}"
        + "QSpinBox{background-color: #1d1d1d}"
        + "QLineEdit{background-color: #1d1d1d}"
        + "QMenu{background-color: #1d1d1d}"
        + "QToolTip{border: 1px solid white; background-color: #1d1d1d; color: #ffffff; font-family: Cambria; font-size: 18px}")
        
        #Main layout
        
        main_window_layout = QGridLayout()
        main_window_layout.setSpacing(10)

        #Groupboxes

        box_1_grid = QGridLayout()
        self.box_1 = QGroupBox("Randomize")
        self.box_1.setLayout(box_1_grid)
        main_window_layout.addWidget(self.box_1, 0, 0, 1, 1)

        box_2_grid = QGridLayout()
        self.box_2 = QGroupBox("Extra")
        self.box_2.setLayout(box_2_grid)
        main_window_layout.addWidget(self.box_2, 0, 1, 1, 1)

        box_3_grid = QGridLayout()
        self.box_3 = QGroupBox("Owned DLC")
        self.box_3.setLayout(box_3_grid)
        main_window_layout.addWidget(self.box_3, 0, 2, 1, 1)

        box_9_grid = QGridLayout()
        self.box_9 = QGroupBox("Length")
        self.box_9.setLayout(box_9_grid)
        main_window_layout.addWidget(self.box_9, 1, 0, 1, 1)

        box_4_grid = QGridLayout()
        self.box_4 = QGroupBox("Output")
        self.box_4.setLayout(box_4_grid)
        main_window_layout.addWidget(self.box_4, 1, 1, 1, 1)

        box_5_grid = QGridLayout()
        self.box_5 = QGroupBox("Platform")
        self.box_5.setLayout(box_5_grid)
        main_window_layout.addWidget(self.box_5, 1, 2, 1, 1)

        box_6_grid = QGridLayout()
        self.box_6 = QGroupBox("Output Path")
        self.box_6.setLayout(box_6_grid)
        main_window_layout.addWidget(self.box_6, 2, 0, 1, 3)
        
        #Checkboxes
        #Randomize

        self.check_box_1 = QCheckBox("Fighter Spirits")
        self.check_box_1.setToolTip("Randomize the placement of battles that unlock fighters.")
        self.check_box_1.stateChanged.connect(self.check_box_1_changed)
        box_1_grid.addWidget(self.check_box_1, 0, 0)

        self.check_box_2 = QCheckBox("Regular Spirits")
        self.check_box_2.setToolTip("Randomize the placement of all standard spirit battles.")
        self.check_box_2.stateChanged.connect(self.check_box_2_changed)
        box_1_grid.addWidget(self.check_box_2, 1, 0)
        
        self.check_box_3 = QCheckBox("Master Spirits")
        self.check_box_3.setToolTip("Randomize the placement of master spirits along\nwith their corresponding activity.")
        self.check_box_3.stateChanged.connect(self.check_box_3_changed)
        box_1_grid.addWidget(self.check_box_3, 2, 0)
        
        self.check_box_23 = QCheckBox("Chest Rewards")
        self.check_box_23.setToolTip("Randomize the pickups found in chests.")
        self.check_box_23.stateChanged.connect(self.check_box_23_changed)
        box_1_grid.addWidget(self.check_box_23, 3, 0)
        
        self.check_box_4 = QCheckBox("Boss Entities")
        self.check_box_4.setToolTip("Shuffle where the 6 sub bosses are fought.")
        self.check_box_4.stateChanged.connect(self.check_box_4_changed)
        box_1_grid.addWidget(self.check_box_4, 4, 0)
        
        self.check_box_26 = QCheckBox("Boss Gimmicks")
        self.check_box_26.setToolTip("Add a random gimmick to every boss fight\nto spice things up.")
        self.check_box_26.stateChanged.connect(self.check_box_26_changed)
        box_1_grid.addWidget(self.check_box_26, 5, 0)
        
        self.check_box_5 = QCheckBox("Skill Tree")
        self.check_box_5.setToolTip("Randomize the placement of skill abilities on the tree.")
        self.check_box_5.stateChanged.connect(self.check_box_5_changed)
        box_1_grid.addWidget(self.check_box_5, 6, 0)
        
        #Extra
        
        self.check_box_22 = QCheckBox("Rebalance FS Meter")
        self.check_box_22.setToolTip("Change the way the final smash meter fills\nup to favor hitting rather than getting hit.\nOnly affects spirit mode.")
        self.check_box_22.stateChanged.connect(self.check_box_22_changed)
        box_2_grid.addWidget(self.check_box_22, 0, 0)
        
        self.check_box_7 = QCheckBox("No Auto DLC")
        self.check_box_7.setToolTip("Disable the mechanic of automatically unlocking\nall DLC characters after 10 battles. Instead they\nwill be added to the overworld.")
        self.check_box_7.stateChanged.connect(self.check_box_7_changed)
        box_2_grid.addWidget(self.check_box_7, 1, 0)
        
        self.check_box_25 = QCheckBox("Short Final Boss")
        self.check_box_25.setToolTip("Remove the initial scrolling stage and boss rush\nfrom the true ending sequence.")
        self.check_box_25.stateChanged.connect(self.check_box_25_changed)
        box_2_grid.addWidget(self.check_box_25, 2, 0)
        
        self.check_box_24 = QCheckBox("Nerf Snacks")
        self.check_box_24.setToolTip("Drastically reduce the experience points from\nthe snack items, making it harder to level spirits up.")
        self.check_box_24.stateChanged.connect(self.check_box_24_changed)
        box_2_grid.addWidget(self.check_box_24, 3, 0)
        
        self.check_box_8 = QCheckBox("Reset Inventory")
        self.check_box_8.setToolTip("Empty your global spirit, core, gold, SP, snack\nand item inventories to start fresh.")
        self.check_box_8.stateChanged.connect(self.check_box_8_changed)
        box_2_grid.addWidget(self.check_box_8, 4, 0)
        
        self.check_box_9 = QCheckBox("Start with Spirits")
        self.check_box_9.setToolTip("Start with 3 primaries and 3 supports in your\nspirit inventory.")
        self.check_box_9.stateChanged.connect(self.check_box_9_changed)
        box_2_grid.addWidget(self.check_box_9, 5, 0)
        
        #DLC
        
        self.check_box_10 = QCheckBox("Piranha Plant")
        self.check_box_10.stateChanged.connect(self.check_box_10_changed)
        box_3_grid.addWidget(self.check_box_10, 0, 0)
        
        self.check_box_11 = QCheckBox("Joker")
        self.check_box_11.stateChanged.connect(self.check_box_11_changed)
        box_3_grid.addWidget(self.check_box_11, 1, 0)
        
        self.check_box_12 = QCheckBox("Hero")
        self.check_box_12.stateChanged.connect(self.check_box_12_changed)
        box_3_grid.addWidget(self.check_box_12, 2, 0)
        
        self.check_box_13 = QCheckBox("Banjo and Kazooie")
        self.check_box_13.stateChanged.connect(self.check_box_13_changed)
        box_3_grid.addWidget(self.check_box_13, 3, 0)
        
        self.check_box_14 = QCheckBox("Terry")
        self.check_box_14.stateChanged.connect(self.check_box_14_changed)
        box_3_grid.addWidget(self.check_box_14, 4, 0)
        
        self.check_box_15 = QCheckBox("Byleth")
        self.check_box_15.stateChanged.connect(self.check_box_15_changed)
        box_3_grid.addWidget(self.check_box_15, 5, 0)
        
        self.check_box_16 = QCheckBox("Min Min")
        self.check_box_16.stateChanged.connect(self.check_box_16_changed)
        box_3_grid.addWidget(self.check_box_16, 6, 0)
        
        self.check_box_17 = QCheckBox("Steve")
        self.check_box_17.stateChanged.connect(self.check_box_17_changed)
        box_3_grid.addWidget(self.check_box_17, 7, 0)
        
        self.check_box_18 = QCheckBox("Sephiroph")
        self.check_box_18.stateChanged.connect(self.check_box_18_changed)
        box_3_grid.addWidget(self.check_box_18, 8, 0)
        
        self.check_box_19 = QCheckBox("Pyra and Mythra")
        self.check_box_19.stateChanged.connect(self.check_box_19_changed)
        box_3_grid.addWidget(self.check_box_19, 9, 0)
        
        self.check_box_20 = QCheckBox("Kazuya")
        self.check_box_20.stateChanged.connect(self.check_box_20_changed)
        box_3_grid.addWidget(self.check_box_20, 10, 0)
        
        self.check_box_21 = QCheckBox("Sora")
        self.check_box_21.stateChanged.connect(self.check_box_21_changed)
        box_3_grid.addWidget(self.check_box_21, 11, 0)
        
        #Radio buttons
        
        self.radio_button_1 = QRadioButton("Raw Params")
        self.radio_button_1.setToolTip("Output all files as regular .prc params.")
        self.radio_button_1.toggled.connect(self.radio_button_group_1_checked)
        box_4_grid.addWidget(self.radio_button_1, 0, 0)
        
        self.radio_button_2 = QRadioButton("Param Patches")
        self.radio_button_2.setToolTip("Output all files as .prcx patches to avoid conflicting\nwith other mods.\nWARNING: Parcel must be installed for this to work.")
        self.radio_button_2.toggled.connect(self.radio_button_group_1_checked)
        box_4_grid.addWidget(self.radio_button_2, 1, 0)
        
        self.radio_button_3 = QRadioButton("Switch")
        self.radio_button_3.setToolTip("Setup the mod for Switch.")
        self.radio_button_3.toggled.connect(self.radio_button_group_2_checked)
        box_5_grid.addWidget(self.radio_button_3, 0, 0)
        
        self.radio_button_4 = QRadioButton("Ryujinx")
        self.radio_button_4.setToolTip("Setup the mod for Ryujinx.")
        self.radio_button_4.toggled.connect(self.radio_button_group_2_checked)
        box_5_grid.addWidget(self.radio_button_4, 1, 0)
        
        #Spinboxes
        
        config.set("Length", "iValue", str(max(min(config.getint("Length", "iValue"), 5), 1)))
        
        self.playthrough_length_field = QSpinBox()
        self.playthrough_length_field.setToolTip("5 is vanilla, anything less will randomly remove\nspirit spots on the map to create a shorter\nplaythrough.")
        self.playthrough_length_field.setRange(1, 5)
        self.playthrough_length_field.setValue(config.getint("Length", "iValue"))
        self.playthrough_length_field.valueChanged.connect(self.playthrough_length_field_changed)
        box_9_grid.addWidget(self.playthrough_length_field, 0, 0)
        
        #Text field

        self.switch_mod_folder_field = QLineEdit(config.get("Misc", "sModFolder"))
        self.switch_mod_folder_field.setPlaceholderText("Mod Folder")
        self.switch_mod_folder_field.textChanged[str].connect(self.switch_mod_folder_field_changed)
        box_6_grid.addWidget(self.switch_mod_folder_field, 0, 0)
        
        self.switch_save_file_field = QLineEdit(config.get("Misc", "sSaveFile"))
        self.switch_save_file_field.setPlaceholderText("Save File")
        self.switch_save_file_field.textChanged[str].connect(self.switch_save_file_field_changed)
        box_6_grid.addWidget(self.switch_save_file_field, 1, 0)
        
        self.ryujinx_folder_field = QLineEdit(config.get("Misc", "sRyujinxFolder"))
        self.ryujinx_folder_field.setPlaceholderText("Ryujinx Folder")
        self.ryujinx_folder_field.textChanged[str].connect(self.ryujinx_folder_field_changed)
        box_6_grid.addWidget(self.ryujinx_folder_field, 0, 0)

        #Buttons
        
        generate_button = QPushButton("Generate")
        generate_button.setToolTip("Patch rom with current settings.")
        generate_button.clicked.connect(self.go_button_clicked)
        main_window_layout.addWidget(generate_button, 4, 0, 1, 3)
        
        self.browse_mod_button = QPushButton()
        self.browse_mod_button.setIcon(QPixmap("Data\\browse.png"))
        self.browse_mod_button.clicked.connect(self.mod_button_clicked)
        box_6_grid.addWidget(self.browse_mod_button, 0, 1)
        
        self.browse_save_button = QPushButton()
        self.browse_save_button.setIcon(QPixmap("Data\\browse.png"))
        self.browse_save_button.clicked.connect(self.save_button_clicked)
        box_6_grid.addWidget(self.browse_save_button, 1, 1)
        
        self.browse_ryujinx_button = QPushButton()
        self.browse_ryujinx_button.setIcon(QPixmap("Data\\browse.png"))
        self.browse_ryujinx_button.clicked.connect(self.ryujinx_button_clicked)
        box_6_grid.addWidget(self.browse_ryujinx_button, 0, 1)
        
        #Seed
        
        self.seed_layout = QGridLayout()
        
        self.seed_field = QLineEdit(config.get("Misc", "sSeed"))
        self.seed_field.setStyleSheet("color: #ffffff")
        self.seed_field.setMaxLength(30)
        self.seed_field.textChanged[str].connect(self.new_seed)
        self.seed_layout.addWidget(self.seed_field, 0, 0, 1, 2)
        
        seed_new_button = QPushButton("New Seed")
        seed_new_button.clicked.connect(self.seed_button_1_clicked)
        self.seed_layout.addWidget(seed_new_button, 1, 0, 1, 1)
        
        seed_confirm_button = QPushButton("Confirm")
        seed_confirm_button.clicked.connect(self.seed_button_2_clicked)
        self.seed_layout.addWidget(seed_confirm_button, 1, 1, 1, 1)
        
        #Init checkboxes
        
        self.check_box_1.setChecked(config.getboolean("Randomize", "bFighterSpirit"))
        self.check_box_2.setChecked(config.getboolean("Randomize", "bSpiritSpirit"))
        self.check_box_3.setChecked(config.getboolean("Randomize", "bMasterSpirit"))
        self.check_box_23.setChecked(config.getboolean("Randomize", "bChestReward"))
        self.check_box_4.setChecked(config.getboolean("Randomize", "bBossEntity"))
        self.check_box_26.setChecked(config.getboolean("Randomize", "bBossGimmick"))
        self.check_box_5.setChecked(config.getboolean("Randomize", "bSkillTree"))
        
        self.check_box_22.setChecked(config.getboolean("Extra", "bRebalanceFSM"))
        self.check_box_7.setChecked(config.getboolean("Extra", "bNoAutoDLC"))
        self.check_box_25.setChecked(config.getboolean("Extra", "bShortTrueEnd"))
        self.check_box_24.setChecked(config.getboolean("Extra", "bNerfSnacks"))
        self.check_box_8.setChecked(config.getboolean("Extra", "bResetSpirit"))
        self.check_box_9.setChecked(config.getboolean("Extra", "bStartSpirit"))
        
        self.check_box_10.setChecked(config.getboolean("DLC", "bPackun"))
        self.check_box_11.setChecked(config.getboolean("DLC", "bJack"))
        self.check_box_12.setChecked(config.getboolean("DLC", "bBrave"))
        self.check_box_13.setChecked(config.getboolean("DLC", "bBuddy"))
        self.check_box_14.setChecked(config.getboolean("DLC", "bDolly"))
        self.check_box_15.setChecked(config.getboolean("DLC", "bMaster"))
        self.check_box_16.setChecked(config.getboolean("DLC", "bTantan"))
        self.check_box_17.setChecked(config.getboolean("DLC", "bPickel"))
        self.check_box_18.setChecked(config.getboolean("DLC", "bEdge"))
        self.check_box_19.setChecked(config.getboolean("DLC", "bElement"))
        self.check_box_20.setChecked(config.getboolean("DLC", "bDemon"))
        self.check_box_21.setChecked(config.getboolean("DLC", "bTrail"))
        
        self.radio_button_1.setChecked(config.getboolean("Output", "bParam"))
        self.radio_button_2.setChecked(config.getboolean("Output", "bPatch"))
        
        self.radio_button_3.setChecked(config.getboolean("Platform", "bSwitch"))
        self.radio_button_4.setChecked(config.getboolean("Platform", "bRyujinx"))
        
        #Window
        
        self.setLayout(main_window_layout)
        self.setFixedSize(1280, 720)
        self.setWindowTitle(script_name)
        self.setWindowIcon(QIcon("Data\\icon.png"))
        
        #Background
        
        background = QPixmap("Data\\background.png")
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, background)
        self.show()
        self.setPalette(self.palette)
        
        #Position
        
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        
        QApplication.processEvents()

    def check_box_1_changed(self):
        checked = self.check_box_1.isChecked()
        config.set("Randomize", "bFighterSpirit", str(checked).lower())

    def check_box_2_changed(self):
        checked = self.check_box_2.isChecked()
        config.set("Randomize", "bSpiritSpirit", str(checked).lower())

    def check_box_3_changed(self):
        checked = self.check_box_3.isChecked()
        config.set("Randomize", "bMasterSpirit", str(checked).lower())

    def check_box_23_changed(self):
        checked = self.check_box_23.isChecked()
        config.set("Randomize", "bChestReward", str(checked).lower())

    def check_box_4_changed(self):
        checked = self.check_box_4.isChecked()
        config.set("Randomize", "bBossEntity", str(checked).lower())

    def check_box_26_changed(self):
        checked = self.check_box_26.isChecked()
        config.set("Randomize", "bBossGimmick", str(checked).lower())

    def check_box_5_changed(self):
        checked = self.check_box_5.isChecked()
        config.set("Randomize", "bSkillTree", str(checked).lower())

    def check_box_22_changed(self):
        checked = self.check_box_22.isChecked()
        config.set("Extra", "bRebalanceFSM", str(checked).lower())

    def check_box_7_changed(self):
        checked = self.check_box_7.isChecked()
        config.set("Extra", "bNoAutoDLC", str(checked).lower())

    def check_box_25_changed(self):
        checked = self.check_box_25.isChecked()
        config.set("Extra", "bShortTrueEnd", str(checked).lower())

    def check_box_24_changed(self):
        checked = self.check_box_24.isChecked()
        config.set("Extra", "bNerfSnacks", str(checked).lower())

    def check_box_8_changed(self):
        checked = self.check_box_8.isChecked()
        config.set("Extra", "bResetSpirit", str(checked).lower())
        if not checked:
            self.check_box_9.setChecked(False)

    def check_box_9_changed(self):
        checked = self.check_box_9.isChecked()
        config.set("Extra", "bStartSpirit", str(checked).lower())
        if checked:
            self.check_box_8.setChecked(True)

    def check_box_10_changed(self):
        checked = self.check_box_10.isChecked()
        config.set("DLC", "bPackun", str(checked).lower())

    def check_box_11_changed(self):
        checked = self.check_box_11.isChecked()
        config.set("DLC", "bJack", str(checked).lower())

    def check_box_12_changed(self):
        checked = self.check_box_12.isChecked()
        config.set("DLC", "bBrave", str(checked).lower())

    def check_box_13_changed(self):
        checked = self.check_box_13.isChecked()
        config.set("DLC", "bBuddy", str(checked).lower())

    def check_box_14_changed(self):
        checked = self.check_box_14.isChecked()
        config.set("DLC", "bDolly", str(checked).lower())

    def check_box_15_changed(self):
        checked = self.check_box_15.isChecked()
        config.set("DLC", "bMaster", str(checked).lower())

    def check_box_16_changed(self):
        checked = self.check_box_16.isChecked()
        config.set("DLC", "bTantan", str(checked).lower())

    def check_box_17_changed(self):
        checked = self.check_box_17.isChecked()
        config.set("DLC", "bPickel", str(checked).lower())

    def check_box_18_changed(self):
        checked = self.check_box_18.isChecked()
        config.set("DLC", "bEdge", str(checked).lower())

    def check_box_19_changed(self):
        checked = self.check_box_19.isChecked()
        config.set("DLC", "bElement", str(checked).lower())

    def check_box_20_changed(self):
        checked = self.check_box_20.isChecked()
        config.set("DLC", "bDemon", str(checked).lower())

    def check_box_21_changed(self):
        checked = self.check_box_21.isChecked()
        config.set("DLC", "bTrail", str(checked).lower())
    
    def radio_button_group_1_checked(self):
        checked_1 = self.radio_button_1.isChecked()
        checked_2 = self.radio_button_2.isChecked()
        config.set("Output", "bParam", str(checked_1).lower())
        config.set("Output", "bPatch", str(checked_2).lower())
    
    def radio_button_group_2_checked(self):
        checked_1 = self.radio_button_3.isChecked()
        checked_2 = self.radio_button_4.isChecked()
        config.set("Platform", "bSwitch",  str(checked_1).lower())
        config.set("Platform", "bRyujinx", str(checked_2).lower())
        self.switch_mod_folder_field.setVisible(checked_1)
        self.browse_mod_button.setVisible(checked_1)
        self.switch_save_file_field.setVisible(checked_1)
        self.browse_save_button.setVisible(checked_1)
        self.ryujinx_folder_field.setVisible(checked_2)
        self.browse_ryujinx_button.setVisible(checked_2)
        self.fix_background_glitch()
    
    def playthrough_length_field_changed(self):
        config.set("Length", "iValue", str(self.playthrough_length_field.value()))
    
    def switch_mod_folder_field_changed(self, mod):
        config.set("Misc", "sModFolder", mod)
    
    def switch_save_file_field_changed(self, save):
        config.set("Misc", "sSaveFile", save)
    
    def ryujinx_folder_field_changed(self, ryujinx):
        config.set("Misc", "sRyujinxFolder", ryujinx)
    
    def fix_background_glitch(self):
        try:
            self.box_1.setStyleSheet("")
            QApplication.processEvents()
            self.setPalette(self.palette)
        except TypeError:
            return
    
    def new_seed(self, text):
        if " " in text:
            self.seed_field.setText(text.replace(" ", ""))
        else:
            config.set("Misc", "sSeed", text)
    
    def cast_seed(self, seed):
        #Cast seed to another object type if possible
        try:
            return float(seed) if "." in seed else int(seed)
        except ValueError:
            return seed
    
    def check_rando_options(self):
        if config.getboolean("Randomize", "bFighterSpirit"):
            return True
        if config.getboolean("Randomize", "bSpiritSpirit"):
            return True
        if config.getboolean("Randomize", "bMasterSpirit"):
            return True
        if config.getboolean("Randomize", "bChestReward"):
            return True
        if config.getboolean("Randomize", "bBossEntity"):
            return True
        if config.getboolean("Randomize", "bSkillTree"):
            return True
        if config.getboolean("Extra", "bStartSpirit"):
            return True
        if config.getint("Length", "iValue") < 5:
            return True
        return False
    
    def set_progress(self, progress):
        self.progress_bar.setValue(progress)
    
    def patch_finished(self):
        box = QMessageBox(self)
        box.setWindowTitle("Done")
        box.setText("Mod generated !")
        box.exec()
        self.setEnabled(True)
    
    def update_finished(self):
        sys.exit()

    def go_button_clicked(self):
        #Check if paths are correct
        
        #Mod folder
        if config.getboolean("Platform", "bSwitch") and config.get("Misc", "sModFolder"):
            if not os.path.isdir(config.get("Misc", "sModFolder")) or os.path.split(config.get("Misc", "sModFolder"))[-1] != "mods":
                self.notify_error("Mod folder path invalid.")
                return
        #Save file
        if config.getboolean("Platform", "bSwitch") and config.get("Misc", "sSaveFile"):
            if not os.path.isfile(config.get("Misc", "sSaveFile")) or os.path.split(config.get("Misc", "sSaveFile"))[-1] != "system_data.bin":
                self.notify_error("Save file path invalid.")
                return
        elif config.getboolean("Extra", "bResetSpirit") and config.getboolean("Platform", "bSwitch"):
            self.notify_error("Save file path required.")
            return
        #Ryujinx folder
        if config.getboolean("Platform", "bRyujinx") and config.get("Misc", "sRyujinxFolder"):
            if not os.path.isdir(config.get("Misc", "sRyujinxFolder")) or os.path.split(config.get("Misc", "sRyujinxFolder"))[-1] != "Ryujinx":
                self.notify_error("Ryujinx folder path invalid.")
                return
        elif config.getboolean("Extra", "bResetSpirit") and config.getboolean("Platform", "bRyujinx"):
            self.notify_error("Ryujinx folder path required.")
            return
        
        #SeedPrompt
        self.seed = ""
        if self.check_rando_options():
            self.seed_box = QDialog(self)
            self.seed_box.setLayout(self.seed_layout)
            self.seed_box.setWindowTitle("Seed")
            self.seed_box.exec()
            if not self.seed:
                return
        
        #Prompt if backup save
        if config.getboolean("Extra", "bResetSpirit"):
            choice = QMessageBox.question(self, "Prompt", "Backup save file ?", QMessageBox.Yes | QMessageBox.No)
            backup = choice == QMessageBox.Yes
        else:
            backup = False
        
        #Start
        
        self.setEnabled(False)
        QApplication.processEvents()
        
        self.progress_bar = QProgressDialog("Generating...", None, 0, 1, self)
        self.progress_bar.setWindowTitle("Status")
        self.progress_bar.setWindowModality(Qt.WindowModal)
        
        self.worker = Generate(self.seed, backup)
        self.worker.signaller.progress.connect(self.set_progress)
        self.worker.signaller.finished.connect(self.patch_finished)
        self.worker.signaller.error.connect(self.thread_failure)
        self.worker.start()
    
    def mod_button_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "Folder")
        if path:
            self.switch_mod_folder_field.setText(path.replace("/", "\\"))
    
    def save_button_clicked(self):
        file = QFileDialog.getOpenFileName(parent=self, caption="File", filter="*.bin")[0]
        if file:
            self.switch_save_file_field.setText(file.replace("/", "\\"))
    
    def ryujinx_button_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "Folder")
        if path:
            self.ryujinx_folder_field.setText(path.replace("/", "\\"))
    
    def seed_button_1_clicked(self):
        self.seed_field.setText(str(random.randint(1000000000, 9999999999)))
    
    def seed_button_2_clicked(self):
        self.seed = self.cast_seed(config.get("Misc", "sSeed"))
        self.seed_box.close()
    
    def thread_failure(self):
        self.progress_bar.close()
        self.setEnabled(True)
        self.notify_error("An error has occured.\nCheck the command window for more detail.")
    
    def notify_error(self, message):
        box = QMessageBox(self)
        box.setWindowTitle("Error")
        box.setIcon(QMessageBox.Critical)
        box.setText(message)
        box.exec()
    
    def check_for_updates(self):
        if os.path.isfile("delete.me"):
            os.remove("delete.me")
        try:
            api = requests.get("https://api.github.com/repos/Lakifume/WoL-Randomizer/releases/latest").json()
        except requests.ConnectionError:
            self.setEnabled(True)
            return
        try:
            tag = api["tag_name"]
        except KeyError:
            self.setEnabled(True)
            return
        if tag != config.get("Misc", "sVersion"):
            choice = QMessageBox.question(self, "Auto Updater", "New version found:\n\n" + api["body"] + "\n\nUpdate ?", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.progress_bar = QProgressDialog("Downloading...", None, 0, api["assets"][0]["size"], self)
                self.progress_bar.setWindowTitle("Status")
                self.progress_bar.setWindowModality(Qt.WindowModal)
                self.progress_bar.setAutoClose(False)
                self.progress_bar.setAutoReset(False)
                
                self.worker = Update(self.progress_bar, api)
                self.worker.signaller.progress.connect(self.set_progress)
                self.worker.signaller.finished.connect(self.update_finished)
                self.worker.signaller.error.connect(self.thread_failure)
                self.worker.start()
            else:
                self.setEnabled(True)
        else:
            self.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(writing)
    main = Main()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()