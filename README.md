# Timeclock
### _Copyright Xavier Mercerweiss 2024, Licensed under GPLv3_

## Overview
A quick and dirty series of Python/Tkinter scripts I created to allow personal timekeeping; facilitates productivity by easily measuring time spent on any given task. Designed and tested exlusively for Debian systems. Output exists as a `entries.csv` and may be viewed/edited using the provided CLI or any consumer spreadsheet tool.

## Installation
Ensure Python 3 and Tkinter are installed and up-to-date before launching.
```bash
$ sudo apt update && sudo apt upgrade
$ sudo apt-get install python3
$ sudo apt-get install python3-tk
```
While Tkinter is part of Python's standard library, some systems may not have tk properly installed. Running these commands before startup should fix any issues.

## Usage
To open the GUI, simply execute `main.py`, with or without the flag `g` or `gui`:
```bash
$ python3 main.py
```
The included CLI can be opened by adding the flag `c` or `cli`:
```bash
$ python3 main.py cli
```

The CLI maintains the following commands:
Command | Usage
--- | ---
`set <path>` | Change which .csv the CLI is accessing. Doesn't need to be used to access the default file `entries.csv`, which is opened on startup.
`print` | View the current .csv file.
`report` | Report the current number of hours spent on each subject, down to one tenth of an hour.
`delete <index>` | Will delete the row of line number `index` from the current .csv file.
`wipe` | Will delete all entries from the current .csv file EXCEPT for the header* row.

*The .csv's header should never be altered by the program, but may be changed manually.
