import os
import configparser
from pathlib import Path
from hbexcel import utils

# Read configuration file
def read_config_file():
    username = os.getlogin()
    user_config = utils.CONFIG_PATH + "/" + username + ".ini"
    config = configparser.ConfigParser()
    res = {}


    path_xhb = utils.DEFAULT_XHB_PATH
    path_excel = utils.DEFAULT_XLS_PATH
    mappings = {}

    try:
        config.read_file(open(user_config))

        if "paths" in config:
            paths = config["paths"]
            path_xhb = Path(paths["path_xhb"]) if "path_xhb" in paths else utils.DEFAULT_XHB_PATH
            path_excel = Path(paths["path_excel"]) if "path_excel" in paths else utils.DEFAULT_XLS_PATH

        if "mappings" in config:
            mappings = config["mappings"]

    except OSError:
        path_xhb = utils.DEFAULT_XHB_PATH
        path_excel = utils.DEFAULT_XLS_PATH
        mappings = {}

    res["Paths"] = (path_xhb, path_excel)
    res["Mappings"] = mappings
    return res


# Print current config information
def print_config_info(xhb_path, xls_path, mappings):
    print("============================================================================")
    print("Configuration currently used by the program")
    print("============================================================================")
    print(f"HomeBank file path stored: {xhb_path}")
    print(f"Excel file path stored: {xls_path}")
    print("\nMappings:")
    for m in mappings:
        print(f"- {m:<35} : {mappings[m]}")
    print("============================================================================")