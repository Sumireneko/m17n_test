#
# Krita multilingualation text by QM file
#
import os, json
from krita import *

try:
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox)
    from PyQt6.QtCore import QTranslator, QCoreApplication
except ImportError:
    from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox)
    from PyQt5.QtCore import QTranslator, QCoreApplication

# PyQt 5->6 Migration Note:
"""
Some Enums names are changed
    PyQt5: Qt.AlignCenter
    PyQt6: Qt.AlignmentFlag.AlignCenter
# self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT6 else Qt.AlignCenter)
exec method changed
    PyQt5: dialog.exec_()
    PyQt6: dialog.exec()
"""

# --- Setting Path ---
QM_FILE_NAME_PREFIX = "my_plugin_" 
DEBUG_MODE = True  
DEBUG_PATH = r"/Users/user/config_path/my_debug_config.json"
DEBUG_BASE_DIR = r"/Users/user/m17n_test/qm"

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
        self.translator = QTranslator()
        
        # 1. Load setting
        settings = load_setting()
        self.current_lang = settings.get("Language", "en_US")
        print(f"--- Initializing --- \nInitial Language: {self.current_lang}")

        self.init_ui()
        # 2. Apply Translation
        self.update_translation(self.current_lang)

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Create UI Elements
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
        
        self.retranslate_ui()
        self.setWindowTitle("Translation Test" + self.current_lang)

    def retranslate_ui(self):
        """ Translation """
        ctx = "TranslationDemo"
        
        # Get current language code from combo-box 
        current_code = self.combo_lang.currentData()

        if current_code == "en_US":
            # --- If en_US, set english source directly,not depend to translation dictionary  ---
            self.lbl_title.setText("Welcome to Krita Plugin")
            self.btn_action.setText("Execute Process")
            self.chk_option.setText("Enable Advanced Mode")
            self.btn_reset.setText("Reset Settings")
            print("Directly set English text (Bypassing Dictionary)")
        else:
            # --- Get from each dictionary  ---
            self.lbl_title.setText(QCoreApplication.translate(ctx, "Welcome to Krita Plugin"))
            self.btn_action.setText(QCoreApplication.translate(ctx, "Execute Process"))
            self.chk_option.setText(QCoreApplication.translate(ctx, "Enable Advanced Mode"))
            self.btn_reset.setText(QCoreApplication.translate(ctx, "Reset Settings"))
            print(f"Applied {current_code} translation from Dictionary")

    def on_lang_changed(self, index):
        lang_code = self.combo_lang.itemData(index)
        print(f"Changing language to: {lang_code}")
        
        self.update_translation(lang_code)
        save_setting({"Language": lang_code})

    def on_reset_clicked(self):
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
        self.combo_lang.setCurrentIndex(self.combo_lang.findData("en_US"))

    def update_translation(self, lang_code):
        app = QCoreApplication.instance()
        MY_OBJ_NAME = "MyUniquePluginTranslator"

        print(f"--- Attempting change to: {lang_code} ---")  

        # 1.Remove all translators that match the name or that this class possesses.
        # It loops through and completely removes its own registered Translator.
        all_translators = app.findChildren(QTranslator)
        for t in all_translators:
            # Check if the name matches, or check for previous rimains (empty names).
            if t.objectName() == MY_OBJ_NAME:
                app.removeTranslator(t)
                t.deleteLater() # Delete from the memory

        # 2. Load a locale
        if lang_code != "en_US":
            base_dir = DEBUG_BASE_DIR if DEBUG_MODE else os.path.dirname(os.path.abspath(__file__))
            qm_filename = f"{QM_FILE_NAME_PREFIX}{lang_code}.qm"
            path = os.path.join(base_dir, qm_filename)

            self.translator = QTranslator() 
            self.translator.setObjectName(MY_OBJ_NAME)

            if os.path.exists(path):
                if self.translator.load(path):
                    app.installTranslator(self.translator)
                    print(f"Successfully installed: {lang_code}")
                else:
                    print(f"Failed to load QM: {path}")
            else:
                print(f"File not found: {path}")
        else:
            # When using en_US, do not install anything.
            # Since everything has been stripped away in step 1, it will automatically revert to English (source).


            print("Cleanup complete: Back to English (Source)")
        
        # 3. UI forced updating
        self.retranslate_ui()

# --- Execution ---
if 'demo_win' in globals():
    demo_win.close()
    demo_win.deleteLater()

demo_win = TranslationDemo()
demo_win.show()
