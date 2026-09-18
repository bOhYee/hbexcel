import openpyxl
from dateutil.relativedelta import relativedelta
from aspose.cells_foss import Workbook, cells


# Take the data retrieved from HomeBank and use the mappings to place them in the Excel sheet
def write_data_to_excel(cli_params, xls_path, time_interval, mappings, categories, operations):
    sdate = time_interval[0]
    if len(time_interval) == 2:
        edate = time_interval[1]
    else:
        edate = time_interval[0]

    if len(mappings) == 0:
        print("[ERROR] No mappings have been provided. Can't proceed with assignments...")
        return -1

    # Try to open the file
    # if it is not an XLS, will raise an exception
    try:
        workbook = Workbook(str(xls_path))
    except Exception as e:
        print(f"[ERROR] Could not open XLS file: {xls_path} {e}")
        return -1

    # Loop through the months
    while sdate <= edate:
        # in case for a specific month there are no transactions, skip
        month = sdate.strftime("%B").strip()
        try:
            month_stats = operations[month]
        except KeyError:
            sdate += relativedelta(months=1)
            continue

        for ws in workbook.worksheets:
            if ws.name == month.capitalize():
                worksheet = ws
                break

        for cat in sorted(categories.keys()):
            amount = 0

            # For that month the category doesnt have any transaction:
            # Put 0 as amount
            # Else use the value retrieved
            if cat in month_stats:
                amount = month_stats[cat]

            category_name = categories[cat]['name']
            parent_key = categories[cat]['parent']
            parent_name = ""
            if parent_key:
                parent_name = categories[parent_key]['name'] + "_"

            # Search if the name of the category:subcategory is present in the received mappings
            # In case it isnt, warning and skip
            name = f"{parent_name}{category_name}".lower()
            if not(name in mappings):
                if amount:
                    print(f"[WARNING] {name.capitalize()} is not present in the mappings provided! Skipping the line...")

                continue

            cell = mappings[name]
            worksheet.cells[cell].value = amount

        sdate += relativedelta(months=1)
        print() 

    if not cli_params["hbex_testmode"]:
        workbook.save(xls_path)
        print("Workbook saved!")