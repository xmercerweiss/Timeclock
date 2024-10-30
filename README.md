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
### Graphical User Interface
The GUI allows you to log the time you've spent on a given ativity.

To open the GUI, simply execute `main.py`, with or without the flag `g` or `gui`:
```bash
$ python3 main.py
```
This should open the following window:

![alt text](https://raw.githubusercontent.com/xmercerweiss/Timeclock/refs/heads/main/media/gui_preview.png "GUI Preview")

The _`Subject`_ field designates the name of the activity associated with a given length of time. If left empty, the _`Subject`_ field of the .csv will be listed as `NULL`. Once you've entered the name of an activity, simply hit the "Start" button to begin keeping your time. The amount of time taken _will not_ be listed in the GUI, as I find this simply induces stress in myself. Alt-tab back to whatever you're doing and focus on that; when you're done, come back and hit "Stop."

**NOTE:** Even if you turn off (not sleep, actually shutoff) your computer without hitting "Stop", the program will _still_ log the entry. Ongoing entries are cached and will be retrieved and logged upon next startup, with their _`END`_ time being the moment the shutoff process began.

### Command Line Interface
The CLI allows you to view a .csv's contents, delete or wipe them, and report the number of hours (down to one tenth) spent on each activity.

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
`delete <int>` | Will delete the row of line number `int` from the current .csv file.
`wipe` | Will delete all entries from the current .csv file EXCEPT for the header* row.

*The .csv's header should never be altered by the program, but may be changed manually.

## Conclusion
Thank you for reading! I work hard on these projects, and knowing someone cared to examine my work means a lot to me. If you have any questions, feel free to reach out to me at mercerweissx@gmail.com.

Happy coding!
