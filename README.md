# Timeclock
### _Copyright Xavier Mercerweiss 2024, Licensed under GPLv3_

## Overview
A quick and dirty series of Python/Tkinter scripts I created to allow personal timekeeping; facilitates productivity by easily measuring time spent on any given task. Designed and tested exlusively for Debian systems. Output exists as a `entries.csv` and may be viewed/edited using the provided CLI or any consumer spreadsheet tool.

## Installation
Ensure Python 3 and Tkinter are installed and up-to-date before launching.
shell:
  $ sudo apt update && sudo apt upgrade
  $ sudo apt-get install python3
  $ sudo apt-get install python3-tk

While Tkinter is part of Python's standard library, some systems may not have tk properly installed. Running these commands before startup should fix any issues.
