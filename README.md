# hbexcel
A small Python utility that reads a HomeBank Desktop `.xhb` file, calculates
monthly totals by category/subcategory, and writes those totals into an
existing Excel workbook.

## Usage
To use the CLI application:
```
$ hbexcel <command> <options>
```

The program makes use of a configuration file stored inside user `.config` folders (`$HOME/.hbexcel/<user>.ini` or `%userprofile%/.hbexcel/<user>.ini`). This is used to specify the location of the HomeBank and Excel database files, thus avoiding an additional, mandatory, argument at every launch of the program. Additionally, mappings to associate data to Excel cells have to be provided to correctly make use of the `transfer` mode.
```
[paths]
path_xhb = /path/to/the/homebank/file
path_xls = /path/to/the/excel/sheet

[mappings]
category_subcategory = cell         
...
```

### Examples
To transfer the data of a range of months to Excel:
```
# To transfer data of a single month
$ hbexcel transfer -d 2026-09 

# To transfer data of multiple months
$ hbexcel transfer -d 2026-09 2026-11

# Transfer data and explicit the database
$ hbexcel transfer -d 2026-09 -db /path/to/homebank

# Test that the transfer will work correctly
$ hbexcel transfer -d 2026-09 --testmode
```

To print within the CLI the data extracted from HomeBank:
```
# Data of a single month
$ hbexcel print -d 2026-09
```

To print the config information:
```
$ hbexcel info
```