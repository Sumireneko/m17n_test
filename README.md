
This project is an experiment of Krita plugin translation

This is a test run from Krita's Scripter. 
Therefore, you can specify a suitable location on your hard drive for the configuration file and translation file.


### in the krita_test_XXX.py
```python
# --- Setting Path ---
TS_FILE_NAME_PREFIX = "my_plugin_"  # .xxx file name
DEBUG_MODE = True  
DEBUG_PATH = r"/Users/user/config_path/my_debug_config.json"
DEBUG_BASE_DIR = r"/Users/user/m17n_test/xxx"
```

The language locale is saved in the config.json file and will be retained the next time it's launched.
Since this is a debug test, the plugin path and config file location are specified manually.
Ideally, the pykrita plugin folder would be assigned to this location. 

With some ingenuity, you should be able to save parameters other than locale data in a JSON file as the config data.
