import sys

import src


GUI_FLAGS = {"gui", "g"}
CLI_FLAGS = {"cli", "c"}


if __name__ == "__main__":
	args = set(a.lower() for a in sys.argv[1:])
	if not args or args & GUI_FLAGS:
		main = src.gui.main
	elif args & CLI_FLAGS:
		main = src.cli.main
	main()
	
