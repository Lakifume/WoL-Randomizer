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

script_name, script_extension = os.path.splitext(os.path.basename(__file__))

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

class Generate(QThread):
    def __init__(self, seed):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.seed = seed
    
    def run(self):
        self.signaller.progress.emit(0)
        
        #Initialize
        Manager.init_variable()
        Manager.load_param()
        Manager.load_json()
        #Get mod directory
        if config.getboolean("Platform", "bSwitch") and config.get("Misc", "sModFolder"):
            mod_dir = config.get("Misc", "sModFolder") + "\\WoL Randomizer"
        elif config.get("Platform", "bRyujinx") and config.get("Misc", "sRyujinxFolder"):
            mod_dir = config.get("Misc", "sRyujinxFolder") + "\\sdcard\\ultimate\\mods\\WoL Randomizer"
        else:
            mod_dir = "WoL Randomizer"
        #Reset mod directory
        if os.path.isdir(mod_dir):
            shutil.rmtree(mod_dir)
        #Initialize mod directory
        for i in list(Manager.all_json["FileToPath"].values()):
            if not os.path.isdir(mod_dir + "\\" + i):
                os.makedirs(mod_dir + "\\" + i)
        if not os.path.isdir(mod_dir + "\\ui\\message"):
            os.makedirs(mod_dir + "\\ui\\message")
        for i in range(3):
            if not os.path.isdir(mod_dir + "\\ui\\replace\\spirits\\spirits_" + str(i)):
                os.makedirs(mod_dir + "\\ui\\replace\\spirits\\spirits_" + str(i))
        #ApplyTweaks
        Manager.apply_default_tweaks()
        Manager.gather_data()
        if config.getboolean("Extra", "bRebalanceFSM"):
            Manager.rebalance_fs_meter()
        if config.getboolean("Extra", "bNoAutoDLC"):
            Manager.no_dlc_unlock()
        #Check DLCs
        if not config.getboolean("DLC", "bPackun"):
            Manager.remove_dlc("piranha_plant")
        if not config.getboolean("DLC", "bJack"):
            Manager.remove_dlc("jack_phantom_thief")
        if not config.getboolean("DLC", "bBrave"):
            Manager.remove_dlc("brave_11")
        if not config.getboolean("DLC", "bBuddy"):
            Manager.remove_dlc("buddy")
        if not config.getboolean("DLC", "bDolly"):
            Manager.remove_dlc("dolly")
        if not config.getboolean("DLC", "bMaster"):
            Manager.remove_dlc("master_1")
        if not config.getboolean("DLC", "bTantan"):
            Manager.remove_dlc("tantan_minmin")
        if not config.getboolean("DLC", "bPickel"):
            Manager.remove_dlc("pickel_steve")
        if not config.getboolean("DLC", "bEdge"):
            Manager.remove_dlc("edge_sephiroth")
        if not config.getboolean("DLC", "bElement"):
            Manager.remove_dlc("element_homura")
        if not config.getboolean("DLC", "bDemon"):
            Manager.remove_dlc("demon_kazuya_mishima_00")
        if not config.getboolean("DLC", "bTrail"):
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
        if config.getboolean("Randomize", "bSkillTree"):
            random.seed(self.seed)
            Manager.randomize_skill()
        Manager.rebalance_spirit(config.getboolean("Randomize", "bBossEntity"))
        if config.getint("Length", "iValue") < 5:
            random.seed(self.seed)
            Manager.shorten_playthrough(config.getint("Length", "iValue"))
        if config.getboolean("Randomize", "bFighterSpirit") or config.getboolean("Randomize", "bSpiritSpirit") or config.getboolean("Randomize", "bMasterSpirit") or config.getboolean("Randomize", "bBossEntity"):
            Manager.patch_spot()
        if config.getboolean("Randomize", "bSpiritSpirit"):
            random.seed(self.seed)
            Manager.patch_requirement()
            Manager.patch_reward()
            Manager.patch_shop()
            Manager.patch_summon()
        if config.getboolean("Randomize", "bMasterSpirit"):
            Manager.patch_master_element()
        if config.getboolean("Randomize", "bBossEntity"):
            Manager.patch_boss_entities()
        Manager.patch_text_entry("msg_campaign", "cam_save_level_sele", str(self.seed))
        Manager.patch_text_entry("msg_campaign", "cam_save_num_area", str(self.seed))
        #Mod files
        Manager.copy_spirit_images(mod_dir)
        Manager.save_param(mod_dir)
        if config.getboolean("Output", "bPatch"):
            Manager.convert_param_to_patch(mod_dir)
        Manager.save_text(mod_dir)
        #Save files
        if config.getboolean("Platform", "bSwitch"):
            if config.getboolean("Extra", "bResetSpirit"):
                #Backup save file
                if backup:
                    if not os.path.isdir("Backup"):
                        os.makedirs("Backup")
                    shutil.copyfile(config.get("Misc", "sSaveFile"), "Backup\\system_data.bin")
                #Modify save file
                Manager.reset_spirit(config.get("Misc", "sSaveFile"))
                if config.getboolean("Extra", "bStartSpirit"):
                    random.seed(self.seed)
                    Manager.start_spirit(config.get("Misc", "sSaveFile"))
        else:
            if config.getboolean("Extra", "bResetSpirit"):
                #The save directory name can differ between users
                for i in os.listdir(config.get("Misc", "sRyujinxFolder") + "\\bis\\user\\save"):
                    if "save_data" in os.listdir(config.get("Misc", "sRyujinxFolder") + "\\bis\\user\\save\\" + i + "\\0"):
                        if "system_data.bin" in os.listdir(config.get("Misc", "sRyujinxFolder") + "\\bis\\user\\save\\" + i + "\\0\\save_data"):
                            save_dir = i
                            break
                #Backup save file
                if backup:
                    if not os.path.isdir("Backup"):
                        os.makedirs("Backup")
                    shutil.copyfile(config.get("Misc", "sRyujinxFolder") + "\\bis\\user\\save\\" + save_dir + "\\0\\save_data\\system_data.bin", "Backup\\system_data.bin")
                #Modify save file
                Manager.reset_spirit(config.get("Misc", "sRyujinxFolder") + "\\bis\\user\\save\\" + save_dir + "\\0\\save_data\\system_data.bin")
                Manager.reset_spirit(config.get("Misc", "sRyujinxFolder") + "\\bis\\user\\save\\" + save_dir + "\\1\\save_data\\system_data.bin")
                if config.getboolean("Extra", "bStartSpirit"):
                    random.seed(self.seed)
                    Manager.start_spirit(config.get("Misc", "sRyujinxFolder") + "\\bis\\user\\save\\" + save_dir + "\\0\\save_data\\system_data.bin")
                    Manager.start_spirit(config.get("Misc", "sRyujinxFolder") + "\\bis\\user\\save\\" + save_dir + "\\1\\save_data\\system_data.bin")
        
        self.signaller.progress.emit(1)
        self.signaller.finished.emit()

class Update(QThread):
    def __init__(self, progressBar, api):
        QThread.__init__(self)
        self.signaller = Signaller()
        self.progressBar = progressBar
        self.api = api

    def run(self):
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
        
        self.progressBar.setLabelText("Extracting...")
        
        #Reset folders
        
        shutil.rmtree("Data\\Json")
        shutil.rmtree("Data\\Param")
        shutil.rmtree("Data\\Texture")
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
        sys.exit()

#Interface

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
        + "QLineEdit[text=\"\"]{color: #666666}"
        + "QMenu{background-color: #1d1d1d}"
        + "QToolTip{border: 0px; background-color: #1d1d1d; color: #ffffff; font-family: Cambria; font-size: 18px}")
        
        #Main layout
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        self.dummy_box = QGroupBox()
        grid.addWidget(self.dummy_box, 4, 0, 1, 3)

        #Groupboxes

        box_1_grid = QGridLayout()
        self.box_1 = QGroupBox("Randomize")
        self.box_1.setLayout(box_1_grid)
        grid.addWidget(self.box_1, 0, 0, 1, 1)

        box_2_grid = QGridLayout()
        self.box_2 = QGroupBox("Extra")
        self.box_2.setLayout(box_2_grid)
        grid.addWidget(self.box_2, 0, 1, 1, 1)

        box_3_grid = QGridLayout()
        self.box_3 = QGroupBox("Owned DLC")
        self.box_3.setLayout(box_3_grid)
        grid.addWidget(self.box_3, 0, 2, 1, 1)

        box_9_grid = QGridLayout()
        self.box_9 = QGroupBox("Length")
        self.box_9.setLayout(box_9_grid)
        grid.addWidget(self.box_9, 1, 0, 1, 1)

        box_4_grid = QGridLayout()
        self.box_4 = QGroupBox("Output")
        self.box_4.setLayout(box_4_grid)
        grid.addWidget(self.box_4, 1, 1, 1, 1)

        box_5_grid = QGridLayout()
        self.box_5 = QGroupBox("Platform")
        self.box_5.setLayout(box_5_grid)
        grid.addWidget(self.box_5, 1, 2, 1, 1)

        box_6_grid = QGridLayout()
        self.box_6 = QGroupBox("Output Path")
        self.box_6.setLayout(box_6_grid)
        grid.addWidget(self.box_6, 2, 0, 1, 3)
        
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
        self.check_box_3.setToolTip("Randomize the placement of master spirits along\nwith their correspoding activity.")
        self.check_box_3.stateChanged.connect(self.check_box_3_changed)
        box_1_grid.addWidget(self.check_box_3, 2, 0)
        
        self.check_box_4 = QCheckBox("Boss Entities")
        self.check_box_4.setToolTip("Shuffle where the 6 sub bosses are fought.")
        self.check_box_4.stateChanged.connect(self.check_box_4_changed)
        box_1_grid.addWidget(self.check_box_4, 3, 0)
        
        self.check_box_5 = QCheckBox("Skill Tree")
        self.check_box_5.setToolTip("Randomize the placement of skill abilities on the tree.")
        self.check_box_5.stateChanged.connect(self.check_box_5_changed)
        box_1_grid.addWidget(self.check_box_5, 4, 0)
        
        #Extra
        
        self.check_box_22 = QCheckBox("Rebalance FS Meter")
        self.check_box_22.setToolTip("Change the way the final smash meter fills\nup to favor hitting rather than getting hit.\nOnly affects spirit mode.")
        self.check_box_22.stateChanged.connect(self.check_box_22_changed)
        box_2_grid.addWidget(self.check_box_22, 0, 0)
        
        self.check_box_7 = QCheckBox("No Auto DLC")
        self.check_box_7.setToolTip("Disable the mechanic of automatically unlocking\nall DLC characters after 10 battles.")
        self.check_box_7.stateChanged.connect(self.check_box_7_changed)
        box_2_grid.addWidget(self.check_box_7, 1, 0)
        
        self.check_box_8 = QCheckBox("Reset Inventory")
        self.check_box_8.setToolTip("Empty your global spirit, core, gold, SP, snack\nand item inventories to start fresh.")
        self.check_box_8.stateChanged.connect(self.check_box_8_changed)
        box_2_grid.addWidget(self.check_box_8, 2, 0)
        
        self.check_box_9 = QCheckBox("Start with Spirits")
        self.check_box_9.setToolTip("Start with 3 primaries and 3 supports in your\nspirit inventory.")
        self.check_box_9.stateChanged.connect(self.check_box_9_changed)
        box_2_grid.addWidget(self.check_box_9, 3, 0)
        
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
        
        if config.getint("Length", "iValue") < 1:
            config.set("Length", "iValue", "1")
        if config.getint("Length", "iValue") > 5:
            config.set("Length", "iValue", "5")
        
        self.length_box = QSpinBox()
        self.length_box.setToolTip("5 is vanilla, anything less will randomly remove\nspirit spots on the map to create a shorter\nplaythrough.")
        self.length_box.setRange(1, 5)
        self.length_box.setValue(config.getint("Length", "iValue"))
        self.length_box.valueChanged.connect(self.new_length)
        box_9_grid.addWidget(self.length_box, 0, 0)
        
        #Text field

        self.mod_field = QLineEdit(config.get("Misc", "sModFolder"))
        self.mod_field.setPlaceholderText("Mod Folder")
        self.mod_field.textChanged[str].connect(self.new_mod)
        box_6_grid.addWidget(self.mod_field, 0, 0)
        
        self.save_field = QLineEdit(config.get("Misc", "sSaveFile"))
        self.save_field.setPlaceholderText("Save File")
        self.save_field.textChanged[str].connect(self.new_save)
        box_6_grid.addWidget(self.save_field, 1, 0)
        
        self.ryujinx_field = QLineEdit(config.get("Misc", "sRyujinxFolder"))
        self.ryujinx_field.setPlaceholderText("Ryujinx Folder")
        self.ryujinx_field.textChanged[str].connect(self.new_ryujinx)
        box_6_grid.addWidget(self.ryujinx_field, 0, 0)

        #Buttons
        
        go_button = QPushButton("Generate")
        go_button.setToolTip("Patch rom with current settings.")
        go_button.clicked.connect(self.go_button_clicked)
        grid.addWidget(go_button, 4, 0, 1, 3)
        
        self.mod_button = QPushButton()
        self.mod_button.setIcon(QPixmap("Data\\browse.png"))
        self.mod_button.clicked.connect(self.mod_button_clicked)
        box_6_grid.addWidget(self.mod_button, 0, 1)
        
        self.save_button = QPushButton()
        self.save_button.setIcon(QPixmap("Data\\browse.png"))
        self.save_button.clicked.connect(self.save_button_clicked)
        box_6_grid.addWidget(self.save_button, 1, 1)
        
        self.ryujinx_button = QPushButton()
        self.ryujinx_button.setIcon(QPixmap("Data\\browse.png"))
        self.ryujinx_button.clicked.connect(self.ryujinx_button_clicked)
        box_6_grid.addWidget(self.ryujinx_button, 0, 1)
        
        #Seed
        
        self.seed_layout = QGridLayout()
        
        self.seed_field = QLineEdit(config.get("Misc", "sSeed"))
        self.seed_field.setStyleSheet("color: #ffffff")
        self.seed_field.setMaxLength(30)
        self.seed_field.textChanged[str].connect(self.new_seed)
        self.seed_layout.addWidget(self.seed_field, 0, 0, 1, 2)
        
        seed_button_1 = QPushButton("New Seed")
        seed_button_1.clicked.connect(self.seed_button_1_clicked)
        self.seed_layout.addWidget(seed_button_1, 1, 0, 1, 1)
        
        seed_button_2 = QPushButton("Confirm")
        seed_button_2.clicked.connect(self.seed_button_2_clicked)
        self.seed_layout.addWidget(seed_button_2, 1, 1, 1, 1)
        
        #Init checkboxes
        
        if config.getboolean("Randomize", "bFighterSpirit"):
            self.check_box_1.setChecked(True)
        if config.getboolean("Randomize", "bSpiritSpirit"):
            self.check_box_2.setChecked(True)
        if config.getboolean("Randomize", "bMasterSpirit"):
            self.check_box_3.setChecked(True)
        if config.getboolean("Randomize", "bBossEntity"):
            self.check_box_4.setChecked(True)
        if config.getboolean("Randomize", "bSkillTree"):
            self.check_box_5.setChecked(True)
        
        if config.getboolean("Extra", "bRebalanceFSM"):
            self.check_box_22.setChecked(True)
        if config.getboolean("Extra", "bNoAutoDLC"):
            self.check_box_7.setChecked(True)
        if config.getboolean("Extra", "bResetSpirit"):
            self.check_box_8.setChecked(True)
        else:
            self.check_box_8_changed()
        if config.getboolean("Extra", "bStartSpirit"):
            self.check_box_9.setChecked(True)
        
        if config.getboolean("DLC", "bPackun"):
            self.check_box_10.setChecked(True)
        if config.getboolean("DLC", "bJack"):
            self.check_box_11.setChecked(True)
        if config.getboolean("DLC", "bBrave"):
            self.check_box_12.setChecked(True)
        if config.getboolean("DLC", "bBuddy"):
            self.check_box_13.setChecked(True)
        if config.getboolean("DLC", "bDolly"):
            self.check_box_14.setChecked(True)
        if config.getboolean("DLC", "bMaster"):
            self.check_box_15.setChecked(True)
        if config.getboolean("DLC", "bTantan"):
            self.check_box_16.setChecked(True)
        if config.getboolean("DLC", "bPickel"):
            self.check_box_17.setChecked(True)
        if config.getboolean("DLC", "bEdge"):
            self.check_box_18.setChecked(True)
        if config.getboolean("DLC", "bElement"):
            self.check_box_19.setChecked(True)
        if config.getboolean("DLC", "bDemon"):
            self.check_box_20.setChecked(True)
        if config.getboolean("DLC", "bTrail"):
            self.check_box_21.setChecked(True)
        
        if config.getboolean("Output", "bParam"):
            self.radio_button_1.setChecked(True)
        else:
            self.radio_button_2.setChecked(True)
        
        if config.getboolean("Platform", "bSwitch"):
            self.radio_button_3.setChecked(True)
        else:
            self.radio_button_4.setChecked(True)
        
        #Window
        
        self.setLayout(grid)
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
        if self.check_box_1.isChecked():
            config.set("Randomize", "bFighterSpirit", "true")
        else:
            config.set("Randomize", "bFighterSpirit", "false")

    def check_box_2_changed(self):
        if self.check_box_2.isChecked():
            config.set("Randomize", "bSpiritSpirit", "true")
        else:
            config.set("Randomize", "bSpiritSpirit", "false")

    def check_box_3_changed(self):
        if self.check_box_3.isChecked():
            config.set("Randomize", "bMasterSpirit", "true")
        else:
            config.set("Randomize", "bMasterSpirit", "false")

    def check_box_4_changed(self):
        if self.check_box_4.isChecked():
            config.set("Randomize", "bBossEntity", "true")
        else:
            config.set("Randomize", "bBossEntity", "false")

    def check_box_5_changed(self):
        if self.check_box_5.isChecked():
            config.set("Randomize", "bSkillTree", "true")
        else:
            config.set("Randomize", "bSkillTree", "false")

    def check_box_22_changed(self):
        if self.check_box_22.isChecked():
            config.set("Extra", "bRebalanceFSM", "true")
        else:
            config.set("Extra", "bRebalanceFSM", "false")

    def check_box_7_changed(self):
        if self.check_box_7.isChecked():
            config.set("Extra", "bNoAutoDLC", "true")
        else:
            config.set("Extra", "bNoAutoDLC", "false")

    def check_box_8_changed(self):
        if self.check_box_8.isChecked():
            config.set("Extra", "bResetSpirit", "true")
        else:
            config.set("Extra", "bResetSpirit", "false")
            self.check_box_9.setChecked(False)

    def check_box_9_changed(self):
        if self.check_box_9.isChecked():
            config.set("Extra", "bStartSpirit", "true")
            self.check_box_8.setChecked(True)
        else:
            config.set("Extra", "bStartSpirit", "false")

    def check_box_10_changed(self):
        if self.check_box_10.isChecked():
            config.set("DLC", "bPackun", "true")
        else:
            config.set("DLC", "bPackun", "false")

    def check_box_11_changed(self):
        if self.check_box_11.isChecked():
            config.set("DLC", "bJack", "true")
        else:
            config.set("DLC", "bJack", "false")

    def check_box_12_changed(self):
        if self.check_box_12.isChecked():
            config.set("DLC", "bBrave", "true")
        else:
            config.set("DLC", "bBrave", "false")

    def check_box_13_changed(self):
        if self.check_box_13.isChecked():
            config.set("DLC", "bBuddy", "true")
        else:
            config.set("DLC", "bBuddy", "false")

    def check_box_14_changed(self):
        if self.check_box_14.isChecked():
            config.set("DLC", "bDolly", "true")
        else:
            config.set("DLC", "bDolly", "false")

    def check_box_15_changed(self):
        if self.check_box_15.isChecked():
            config.set("DLC", "bMaster", "true")
        else:
            config.set("DLC", "bMaster", "false")

    def check_box_16_changed(self):
        if self.check_box_16.isChecked():
            config.set("DLC", "bTantan", "true")
        else:
            config.set("DLC", "bTantan", "false")

    def check_box_17_changed(self):
        if self.check_box_17.isChecked():
            config.set("DLC", "bPickel", "true")
        else:
            config.set("DLC", "bPickel", "false")

    def check_box_18_changed(self):
        if self.check_box_18.isChecked():
            config.set("DLC", "bEdge", "true")
        else:
            config.set("DLC", "bEdge", "false")

    def check_box_19_changed(self):
        if self.check_box_19.isChecked():
            config.set("DLC", "bElement", "true")
        else:
            config.set("DLC", "bElement", "false")

    def check_box_20_changed(self):
        if self.check_box_20.isChecked():
            config.set("DLC", "bDemon", "true")
        else:
            config.set("DLC", "bDemon", "false")

    def check_box_21_changed(self):
        if self.check_box_21.isChecked():
            config.set("DLC", "bTrail", "true")
        else:
            config.set("DLC", "bTrail", "false")
    
    def radio_button_group_1_checked(self):
        if self.radio_button_1.isChecked():
            config.set("Output", "bParam", "true")
            config.set("Output", "bPatch", "false")
        else:
            config.set("Output", "bParam", "false")
            config.set("Output", "bPatch", "true")
    
    def radio_button_group_2_checked(self):
        if self.radio_button_3.isChecked():
            config.set("Platform", "bSwitch", "true")
            config.set("Platform", "bRyujinx", "false")
            self.mod_field.setVisible(True)
            self.mod_button.setVisible(True)
            self.save_field.setVisible(True)
            self.save_button.setVisible(True)
            self.ryujinx_field.setVisible(False)
            self.ryujinx_button.setVisible(False)
        else:
            config.set("Platform", "bSwitch", "false")
            config.set("Platform", "bRyujinx", "true")
            self.mod_field.setVisible(False)
            self.mod_button.setVisible(False)
            self.save_field.setVisible(False)
            self.save_button.setVisible(False)
            self.ryujinx_field.setVisible(True)
            self.ryujinx_button.setVisible(True)
        self.fix_background_glitch()
    
    def new_length(self):
        config.set("Length", "iValue", str(self.length_box.value()))
    
    def new_mod(self, mod):
        if mod:
            self.mod_field.setStyleSheet("color: #ffffff")
        else:
            self.mod_field.setStyleSheet("color: #666666")
        config.set("Misc", "sModFolder", mod)
        self.fix_background_glitch()
    
    def new_save(self, save):
        if save:
            self.save_field.setStyleSheet("color: #ffffff")
        else:
            self.save_field.setStyleSheet("color: #666666")
        config.set("Misc", "sSaveFile", save)
        self.fix_background_glitch()
    
    def new_ryujinx(self, ryujinx):
        if ryujinx:
            self.ryujinx_field.setStyleSheet("color: #ffffff")
        else:
            self.ryujinx_field.setStyleSheet("color: #666666")
        config.set("Misc", "sRyujinxFolder", ryujinx)
        self.fix_background_glitch()
    
    def fix_background_glitch(self):
        try:
            self.dummy_box.setStyleSheet("")
            QApplication.processEvents()
            self.setPalette(self.palette)
        except TypeError:
            return
    
    def new_seed(self, text):
        if " " in text:
            self.seed_field.setText(text.replace(" ", ""))
        else:
            config.set("Misc", "sSeed", text)
    
    def check_rando_options(self):
        if config.getboolean("Randomize", "bFighterSpirit"):
            return True
        if config.getboolean("Randomize", "bSpiritSpirit"):
            return True
        if config.getboolean("Randomize", "bMasterSpirit"):
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
        self.progressBar.setValue(progress)
    
    def patch_finished(self):
        box = QMessageBox(self)
        box.setWindowTitle("Done")
        box.setText("Mod generated !")
        box.exec()
        self.setEnabled(True)

    def go_button_clicked(self):
        #Check if paths are correct
        #Mod folder
        if config.getboolean("Platform", "bSwitch") and config.get("Misc", "sModFolder"):
            if not os.path.isdir(config.get("Misc", "sModFolder")) or config.get("Misc", "sModFolder").split("\\")[-1] != "mods":
                self.no_path("Mod folder path invalid.")
                self.setEnabled(True)
                return
        #Save file
        if config.getboolean("Platform", "bSwitch") and config.get("Misc", "sSaveFile"):
            if not os.path.isfile(config.get("Misc", "sSaveFile")) or config.get("Misc", "sSaveFile").split("\\")[-1] != "system_data.bin":
                self.no_path("Save file path invalid.")
                self.setEnabled(True)
                return
        elif config.getboolean("Extra", "bResetSpirit") and config.getboolean("Platform", "bSwitch"):
            self.no_path("Save file path required.")
            self.setEnabled(True)
            return
        #Ryujinx folder
        if config.getboolean("Platform", "bRyujinx") and config.get("Misc", "sRyujinxFolder"):
            if not os.path.isdir(config.get("Misc", "sRyujinxFolder")) or config.get("Misc", "sRyujinxFolder").split("\\")[-1] != "Ryujinx":
                self.no_path("Ryujinx folder path invalid.")
                self.setEnabled(True)
                return
        elif config.getboolean("Extra", "bResetSpirit") and config.getboolean("Platform", "bRyujinx"):
            self.no_path("Ryujinx folder path required.")
            self.setEnabled(True)
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
        
        #Cast seed to another object type if possible
        #By default it is a string
        try:
            if "." in self.seed:
                self.seed = float(self.seed)
            else:
                self.seed = int(self.seed)
        except ValueError:
            pass
        
        #Prompt if backup save
        global backup
        if config.getboolean("Extra", "bResetSpirit"):
            choice = QMessageBox.question(self, "Prompt", "Backup save file ?", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                backup = True
            elif choice == QMessageBox.No:
                backup = False
        else:
            backup = False
        
        #Start
        
        self.setEnabled(False)
        QApplication.processEvents()
        
        self.progressBar = QProgressDialog("Generating...", None, 0, 1, self)
        self.progressBar.setWindowTitle("Status")
        self.progressBar.setWindowModality(Qt.WindowModal)
        
        self.worker = Generate(self.seed)
        self.worker.signaller.progress.connect(self.set_progress)
        self.worker.signaller.finished.connect(self.patch_finished)
        self.worker.start()
    
    def mod_button_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "Folder")
        if path:
            self.mod_field.setText(path.replace("/", "\\"))
    
    def save_button_clicked(self):
        file = QFileDialog.getOpenFileName(parent=self, caption="File", filter="*.bin")[0]
        if file:
            self.save_field.setText(file.replace("/", "\\"))
    
    def ryujinx_button_clicked(self):
        path = QFileDialog.getExistingDirectory(self, "Folder")
        if path:
            self.ryujinx_field.setText(path.replace("/", "\\"))
    
    def seed_button_1_clicked(self):
        self.seed_field.setText(str(random.randint(1000000000, 9999999999)))
    
    def seed_button_2_clicked(self):
        self.seed = config.get("Misc", "sSeed")
        self.seed_box.close()
    
    def no_path(self, message):
        box = QMessageBox(self)
        box.setWindowTitle("Path")
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
            choice = QMessageBox.question(self, "Auto Updater", "New version found:\n\n" + api["body"] + "\n\nWARNING: this will overwrite every file except for the contents of the Mod folder, make backups if you've customized anything.\n\nUpdate ?", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.progressBar = QProgressDialog("Downloading...", None, 0, api["assets"][0]["size"], self)
                self.progressBar.setWindowTitle("Status")
                self.progressBar.setWindowModality(Qt.WindowModal)
                self.progressBar.setAutoClose(False)
                self.progressBar.setAutoReset(False)
                
                self.worker = Update(self.progressBar, api)
                self.worker.signaller.progress.connect(self.set_progress)
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