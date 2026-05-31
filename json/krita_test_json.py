#
# Krita multilingualation text by JSON file
#
import os, json
from krita import *

try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox)
    from PyQt6.QtCore import QCoreApplication
except ImportError:
    from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox)
    from PyQt5.QtCore import QCoreApplication

# --- Setting Path ---
TS_FILE_NAME_PREFIX = "my_plugin_"  # json file name
DEBUG_MODE = True  
DEBUG_PATH = r"/Users/user/config_path/my_debug_config.json"
DEBUG_BASE_DIR = r"/User/user/m17n_test/json"

def get_config_path():
    if DEBUG_MODE: return DEBUG_PATH
    try:
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        plugin_dir = os.path.expanduser("~")
    return os.path.join(plugin_dir, "config.json")

CONFIG_PATH = get_config_path()

def save_setting(data):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e: print(f"Save Error: {e}")

def load_setting():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return {"Language": "en_US"}

# --- Main Class ---

class TranslationDemo(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Load setting
        settings = load_setting()
        self.current_lang = settings.get("Language", "en_US")
        
        # Translation cache dictionary
        self.trans_map = {}

        self.init_ui()
        # 2. Apply Translation
        self.update_translation(self.current_lang)

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.lbl_title = QLabel()
        self.btn_action = QPushButton()
        self.chk_option = QCheckBox()
        
        self.combo_lang = QComboBox()
        self.combo_lang.addItem("English", "en_US")
        self.combo_lang.addItem("日本語", "ja_JP")
        self.combo_lang.addItem("中国語", "zh_CN")
        
        idx = self.combo_lang.findData(self.current_lang)
        if idx >= 0: self.combo_lang.setCurrentIndex(idx)
        
        self.combo_lang.currentIndexChanged.connect(self.on_lang_changed)

        self.btn_reset = QPushButton()
        self.btn_reset.clicked.connect(self.on_reset_clicked)

        self.layout.addWidget(self.lbl_title)
        self.layout.addWidget(self.btn_action)
        self.layout.addWidget(self.chk_option)
        self.layout.addWidget(QLabel("--- Change Language ---"))
        self.layout.addWidget(self.combo_lang)
        self.layout.addWidget(self.btn_reset)
        
        # Fist time
        self.retranslate_ui()

    def tr_custom(self, source_text):
 
        # If it's in the dictionary, it returns that; otherwise, it returns the source code as is.
        return self.trans_map.get(source_text, source_text)

    def retranslate_ui(self):
        """ UI text update """
        self.lbl_title.setText(self_tr := self.tr_custom("Welcome to Krita Plugin"))
        self.btn_action.setText(self.tr_custom("Execute Process"))
        self.chk_option.setText(self.tr_custom("Enable Advanced Mode"))
        self.btn_reset.setText(self.tr_custom("Reset Settings"))
        self.setWindowTitle(self.tr_custom("Translation Test") + f" ({self.current_lang})")

    def on_lang_changed(self, index):
        lang_code = self.combo_lang.itemData(index)
        self.update_translation(lang_code)
        save_setting({"Language": lang_code})

    def on_reset_clicked(self):
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
        self.combo_lang.setCurrentIndex(self.combo_lang.findData("en_US"))

    def update_translation(self, lang_code):
        self.current_lang = lang_code
        print(f"--- Switching to JSON: {lang_code} ---")  
    
        if lang_code == "en_US":
            self.trans_map = {}
        else:
            # Make a path (e.g. my_plugin_ja_JP.json)
            base_dir = DEBUG_BASE_DIR if DEBUG_MODE else os.path.dirname(os.path.abspath(__file__))
            json_filename = f"{TS_FILE_NAME_PREFIX}{lang_code}.json"
            path = os.path.join(base_dir, json_filename)
            
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        self.trans_map = json.load(f)
                    print(f"Successfully loaded JSON: {path}")
                except Exception as e:
                    print(f"JSON Load Error: {e}")
                    self.trans_map = {}
            else:
                print(f"JSON File not found: {path}")
                self.trans_map = {}
    
        self.retranslate_ui()













# --- Execution ---
if 'demo_win' in globals():
    demo_win.close()
    demo_win.deleteLater()

demo_win = TranslationDemo()
demo_win.show()