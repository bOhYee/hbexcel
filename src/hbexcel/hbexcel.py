import sys
import argparse

from pathlib import Path
from datetime import datetime

from hbexcel import utils
from hbexcel import config_manager
from hbexcel import xhb_manager
from hbexcel import xls_manager

# Main program
def main():
    utils.bootstrap()

    # Read configuration file for integrating custom properties
    configs = config_manager.read_config_file()
    
    # Parse arguments received by the program
    parsed_args = parse_arguments(sys.argv[1:])
    if parsed_args["mode"] == utils.ProgramModes.INFO.value:
        config_manager.print_config_info(configs['Paths'][0], configs['Paths'][1], configs["Mappings"])
        return

    dates = parsed_args['hbex_date']
    xhb_path = parsed_args['hbex_xhb'] or configs['Paths'][0]
    if not xhb_path:
        print("[ERROR] Homebank database path was not specified...")
        sys.exit()

    if not xhb_path.is_file():
        print("[ERROR] Homebank database path does not point to a file...")
        sys.exit()

    categories, operations = xhb_manager.parse_xhb(xhb_path, dates)
    if parsed_args["mode"] == utils.ProgramModes.PRINT.value:
        xhb_manager.print_total_per_month(dates, categories, operations)

    elif parsed_args["mode"] == utils.ProgramModes.TRANSFER.value:
        xls_path = parsed_args['hbex_xls'] or configs['Paths'][1]
        if not xls_path:
            print("[ERROR] Excel sheet path was not specified...")
            sys.exit()

        if not xls_path.is_file():
            print("[ERROR] Excel sheet path does not point to a file...")
            sys.exit()

        xls_manager.write_data_to_excel(parsed_args, xls_path, dates, configs["Mappings"], categories, operations)


# Parses the arguments received by the program
def parse_arguments(params):
    app_name = "hbexcel"
    desc = "A simple python program to plug Homebank's data inside .xls files"
    parser = argparse.ArgumentParser(prog=app_name, description=desc)
    subparser = parser.add_subparsers(dest="mode", required=True, help="'subcommand' help")

    parser_info = subparser.add_parser(utils.ProgramModes.INFO.value, help="Print information regarding paths and mappings")

    parser_print = subparser.add_parser(utils.ProgramModes.PRINT.value, help="Print the HomeBank data to CLI")
    parser_print.add_argument("-d", "--date", dest="hbex_date", metavar="DATE", nargs="+", type=utils.parse_date, action=utils.DateProcessor, help="Dates to constrain the information to handle", required=True)
    parser_print.add_argument("-db", "--database", dest="hbex_xhb", metavar="XHB PATH", type=Path, help="Path to the Homebank file")

    parser_scan = subparser.add_parser(utils.ProgramModes.TRANSFER.value, help="Scan the HomeBank file and transfer data to Excel")
    parser_scan.add_argument("-d", "--date", dest="hbex_date", metavar="DATE", nargs="+", type=utils.parse_date, action=utils.DateProcessor, help="Dates to constrain the information to handle", required=True)
    parser_scan.add_argument("-db", "--database", dest="hbex_xhb", metavar="XHB PATH", type=Path, help="Path to the Homebank file")
    parser_scan.add_argument("-t", "--testmode", dest="hbex_testmode", action="store_true", help="Dry-run for the data transfer")
    parser_scan.add_argument("-xls", "--excel", dest="hbex_xls", metavar="XLS PATH", type=Path, help="Path to the Excel sheet")

    res = vars(parser.parse_args(params))
    return res


if __name__ == '__main__':
    main()