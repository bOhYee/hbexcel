import os
import argparse
import shutil
import platformdirs
import locale
from pathlib import Path
from datetime import datetime
from enum import Enum

# Set locale to get months names in local language
locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")

# Path of the src directory
SRC_PATH = Path(__file__).resolve().parent.parent
REPO_PATH = SRC_PATH.parent
CFG_REPO_PATH = REPO_PATH / "config" / "config.ini"

# Paths for the application (platform-dependent)
CONFIG_PATH = platformdirs.user_config_dir("hbexcel", ensure_exists=True)    # Configuration file

# Defaults
DEFAULT_XHB_PATH = None
DEFAULT_XLS_PATH = None

# Program modalities
# Each one is associated to a different type of execution
class ProgramModes(Enum):
    INFO        = "info"         # Print information regarding paths and mappings
    PRINT       = "print"        # Print filtered data from HomeBank xhb file
    TRANSFER    = "transfer"     # Scan the HomeBank file and update the Excel sheet


# Bootstrap procedure
def bootstrap():
    username = os.getlogin()
    user_config = CONFIG_PATH + "/" + username + ".ini"

    if not os.path.exists(user_config):
        shutil.copy2(CFG_REPO_PATH, user_config)


# Parse the date argument
# Date assumed with the format 'YYYY-MM'
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m').date()
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_str}. Use 'YYYY-MM'.")


# For argparse usage
# Used for correctly interpreting how many dates have been written by user
class DateProcessor(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if not 1 <= len(values) <= 2:
            msg = 'argument requires at least one date and a maximum of two dates'
            raise argparse.ArgumentTypeError(msg)

        if len(values) == 2:
            sdate = values[0]
            edate = values[1]

            if values[0] > values[1]:
                msg = f'time interval bounds not well defined. Starting date {sdate} is greater than ending date {edate}'
                raise argparse.ArgumentTypeError(msg)

            # Time period is one year maximum for the Excel sheet
            months_diff = (edate.year - sdate.year) * 12 + (edate.month - sdate.month)
            if len(values) == 2 and months_diff > 12:
                msg = 'maximum supported date difference by the excel sheet is one year'
                raise argparse.ArgumentTypeError(msg)

            # Time period goes from September to August
            if edate.month > 9:
                print("[WARNING] Time period goes from September to August. Ending date has been reduced to match this constraint...")
                edate = edate.replace(month=8)

            values[1] = edate

        setattr(namespace, self.dest, values)