import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from calendar import monthrange
from dateutil.relativedelta import relativedelta


# Read the Homebank XHB file
def parse_xhb(xhb_path, time_interval):
    # Try to open the file
    # if it is not an XHB, will raise an exception
    try:
        root = ET.parse(xhb_path).getroot()
    except ET.ParseError as exc:
        print(f"[ERROR] Could not parse XHB XML: {exc}")
        return -1

    categories = get_categories(root)
    operations = get_operations(root, time_interval)
    return categories, operations


# Parse the XHB and retrieve the categories
def get_categories(xml_root):
    categories = {}
    cat_name = None
    key = None
    parent_key = None

    for element in xml_root.iter():
        if element.tag.lower() != "cat":
            continue

        cat_name = element.attrib['name']
        key = element.attrib['key']
        parent_key = element.attrib['parent'] if "parent" in element.attrib else None

        categories[key] = {
            "name": cat_name,
            "parent": parent_key
        }

    return categories


# Parse the XHB and retrieve the operations within the selected time period
def get_operations(xml_root, time_interval):
    operations = {}
    for element in xml_root.iter():
        if element.tag.lower() != "ope" or not ("category" in element.attrib or "scat" in element.attrib):
            continue

        category_list = []
        amount_list = []

        # Need to filter based on the selected time period
        ope_date = datetime.fromordinal(int(element.attrib['date']))
        fday = time_interval[0].replace(day=1)
        if len(time_interval) == 1:
            lday = time_interval[0].replace(day=monthrange(time_interval[0].year, time_interval[0].month)[1])
        else:
            lday = time_interval[1].replace(day=monthrange(time_interval[1].year, time_interval[1].month)[1])

        if not (fday <= ope_date.date() <= lday):
            continue

        # Operations can also have multiple categories and amounts
        if "scat" in element.attrib:
            category_list = element.attrib["scat"].split("||")
            amount_list = [float(x) for x in element.attrib["samt"].split("||")]
        else:
            category_list.append(element.attrib['category'])
            amount_list.append(float(element.attrib['amount']))

        # Get month name from operation date
        month = ope_date.strftime("%B")
        if not (month in operations):
            operations[month] = {} 

        for (cat, amt) in zip(category_list, amount_list):
            operations[month][cat] = (amt + operations[month][cat]) if cat in operations[month] else amt

    return operations


# Print the total for each category of each month
def print_total_per_month(time_interval, categories, operations):
    sdate = time_interval[0]
    if len(time_interval) == 2:
        edate = time_interval[1]
    else:
        edate = time_interval[0]

    # Loop through the months
    while sdate <= edate:
        month = sdate.strftime("%B")
        try:
            month_stats = operations[month]
        except KeyError:
            sdate += relativedelta(months=1)
            continue

        print(f"=========================================")
        print(f" Expenses for month: {month.capitalize()}")
        print(f"=========================================")

        for cat in sorted(categories.keys()):
            category_name = categories[cat]['name']
            parent_key = categories[cat]['parent']
            parent_name = ""
            if parent_key:
                parent_name = categories[parent_key]['name'] + ":"

            if cat in month_stats:
                name = f"{parent_name}{category_name}"
                print(f" - {name:<30} = {month_stats[cat]:.2f}")

        sdate += relativedelta(months=1)
        print()
