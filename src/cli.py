import inspect
import os


PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)

PROMPT = "?> "
ERR_PUNC = "!!"

AFFIRMATIVE_RESPONSES = {
	"yes",
	"y"
}


WIPE_PROMPT_1_MSG = "{} will be WIPED COMPLETELY! Are you sure? [y/N]: "
WIPE_PROMPT_2_MSG = "Are you SURE you want to wipe this file? [y/N]: "
CURRENT_CSV_MSG = "Current CSV: {}"

MISSING_ARG_ERR_MSG = f"{ERR_PUNC} Command {'{}'} missing one or more arguments {ERR_PUNC}"
INV_CMD_ERR_MSG = f"{ERR_PUNC} Invalid command \"{'{}'}\" {ERR_PUNC}"
MISC_ERR_MSG = f"{ERR_PUNC} Encountered \"{'{}'}\" exception {ERR_PUNC}"

SEP = "-"
WALL = "|"
BLANK = " "
DELIM = ","
NEWLINE = "\n"
WILDCARD = "*"
INTERSECT = "+"
BLANK_CELL = "{}"
CELL_FORMAT = f" {BLANK_CELL} {WALL}"

is_running = True
csv_path = os.path.abspath("entries.csv")


# Main function at top for readability,
# however mainloop is placed at end in order
# to allow reference to all functions above it
def main():
	mainloop()

		
def print_csv():
	table = get_csv_entries(with_indices=True)
	print(table_to_str(table))
		
		
def set_csv_path(path):
	abs_path = os.path.abspath(path)
	if not os.path.isfile(abs_path):
		raise FileNotFoundError()
	global csv_path
	csv_path = abs_path
	
	
def delete_data(inp):
	if inp == WILDCARD:
		wipe_csv()
	else:
		index = int(inp)
		delete_row(index)
	print_csv()
		
		
def wipe_csv():
	first = input(WIPE_PROMPT_1_MSG.format(csv_path))
	if first.strip().lower() not in AFFIRMATIVE_RESPONSES:
		return
	second = input(WIPE_PROMPT_2_MSG)
	if second.strip().lower() not in AFFIRMATIVE_RESPONSES:
		return
	title = get_csv_entries(split=False)[0]
	with open(csv_path, "w") as csv:
		csv.write(title)
	
	
def delete_row(index):
	rows = get_csv_entries(split=False)
	with open(csv_path, "w") as csv:
		for i, r in enumerate(rows):
			if i == 0 or i != index:
				csv.write(r)
				

# This code is really sloppy, as this project has grown
# a lot more than I thought it would, so this is my Q&D
# implementation. Sorry future me ¯\_(ツ)_/¯
def report_hours():
	totals = {}
	max_len = 0
	for subject, _, _, mins in get_csv_entries()[1:]:
		subj_len = len(subject)
		max_len = subj_len if subj_len > max_len else max_len 
		if subject not in totals.keys():
			totals[subject] = 0
		totals[subject] += int(mins)
	
	report = []
	for k, v in totals.items():
		hours = float(v / 60)
		report.append(f"{k:{max_len}} : {hours:.1f} hours")
	report.sort(key=lambda x: float(x.split()[-2]), reverse=True)
	
	for l in report:
		print(l)


def get_csv_entries(split=True, with_indices=False):
	rows = []
	with open(csv_path, "r") as csv:
		for i, l in enumerate(csv.readlines()):
			stripped = l.strip()
			if stripped:
				if split:
					cells = [*stripped.split(DELIM)]
					if with_indices:
						cells.insert(0, str(i))
					rows.append(tuple(cells))
				else:
					row = l
					if with_indices:
						row = f"{i}{DELIM}" + row
					rows.append(row)
	return tuple(rows)
	
	
def table_to_str(table):
	mut = []
	col_sizes = size_columns(table)
	row_format = generate_row_format(len(table[0]), col_sizes)
	for i, row in enumerate(table):
		append_sep = i == 0
		mut.append(
			row_to_str(row, row_format, append_sep)
		)
	return NEWLINE.join(mut)
	
	
def size_columns(table):
	output = [0 for x in table[0]]
	for row in table:
		for i, cell in enumerate(row):
			length = len(str(cell))
			if length > output[i]:
				output[i] = length
	return output
		
		
def row_to_str(row, form=None, with_separator=False):
	print_format = generate_row_format(len(row)) if form is None else form
	output = print_format.format(*row)
	if with_separator:
		separator = generate_separator(output)
		output += NEWLINE + separator
	return output
	
	
def generate_row_format(length, sizes=None):
	blank_format = (CELL_FORMAT * length)[:-1]
	if sizes is None:
		return blank_format

	size_formatters = ["{:%ds}" % size for size in sizes]
	sized_format = blank_format
	for f in size_formatters:
		sized_format = sized_format.replace(BLANK_CELL, f, 1)
	return sized_format
	
	
def generate_separator(row):
	output = ""
	length = len(row)
	intersections = [i for i, c in enumerate(row) if c == WALL]
	old = 0
	for index in intersections:
		new = index - old
		output += (SEP * new) + INTERSECT
		old = index + 1
	else:
		output += SEP * (length - old)
	return output
	

# COMMANDS hashmap placed after function 
# declarations in order to reference all 
# functions. displace_cmd function placed
# below COMMANDS in order to reference it
COMMANDS = {
	"set":		set_csv_path,
	"print":	print_csv,
	"delete":	delete_data,
	"wipe":		wipe_csv,
	"report":	report_hours
}

EXIT_COMMANDS = {
	"exit",
	"e",
	"quit",
	"q"
}
		

def dispatch_cmd(cmd):
	if cmd in EXIT_COMMANDS:
		exit()
	return COMMANDS[cmd]
		
		
def format_args(func, *args):
	needed = len(inspect.signature(func).parameters)
	given = len(args)
	if needed < given:
		return args[:needed]
	elif needed > given:
		raise IndexError()
	else:
		return args
		
# Main function at top for readability,
# however mainloop is placed at end in order
# to allow reference to all functions above it
def mainloop():
	
	while is_running:
		print()
		print(CURRENT_CSV_MSG.format(csv_path))
	
		try:
			cmd, *args = input(PROMPT).lower().strip().split()
			func = dispatch_cmd(cmd)
			formatted = format_args(func, *args)
			func(*formatted)
	
		except KeyError:
			print(
				INV_CMD_ERR_MSG.format(cmd)
			)
		except IndexError:
			print(
				MISSING_ARG_ERR_MSG.format(cmd)
			)
		
		except Exception as e:
			print(
				MISC_ERR_MSG.format(e.__class__.__name__)
			)
	
		
if __name__ == "__main__":
	main()

