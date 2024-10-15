import sys

import src


GUI_FLAGS = {"gui", "g"}
CLI_FLAGS = {"cli", "c"}


INVALID_FLAG_ERR_MSG = \
"""
Invalid flag provided; please only use the following flags:

g, gui	:	Open Timeclock's GUI, allowing entries to be added to the selected .csv file.
c, cli	:	Open Timeclock's CLI, allowing viewing and editing of any .csv file.
"""


def invalid_flag():
	print(INVALID_FLAG_ERR_MSG)

if __name__ == "__main__":
	args = set(a.lower() for a in sys.argv[1:])
	if not args or args & GUI_FLAGS:
		main = src.gui.main
	elif args & CLI_FLAGS:
		main = src.cli.main
	else:
		main = invalid_flag
	main()
	
