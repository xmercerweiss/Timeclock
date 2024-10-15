import datetime as dt
import subprocess
import traceback
import os

from tkinter import ttk
import tkinter as tk


PROJECT_DIR = os.path.dirname(__file__)
os.chdir(PROJECT_DIR)

CSV_PATH = os.path.abspath("entries.csv")
LOG_PATH = os.path.abspath("log.txt")
ICON_PATH = os.path.abspath("../media/icon.png")
START_CACHE_PATH = os.path.abspath(".startcache")

DATETIME_FORMAT = "%m/%d/%Y %I:%M %p"
SHUTDOWN_FORMAT = "%Y %b %d %H:%M"
YEAR_FORMAT = "%Y"
ENTRY_FORMAT = "{},{},{},{}\n"

WINDOW_NAME = "Timeclock"
WINDOW_GEO = "600x480"

ENABLED = "normal"
DISABLED = "disabled"
MARGIN = 50
NULL_STR = "NULL"
CHAR_ENCODING = "utf-8"

ENTRY_PLACEHOLDER = "Subject"
ENTRY_FOCUSED_FG = "black"
ENTRY_FOCUSED_FONT = "helvetica 14"
ENTRY_UNFOCUSED_FONT = f"{ENTRY_FOCUSED_FONT} italic"
ENTRY_UNFOCUSED_FG = "#6f6e6e"

START_BTN_CONFIG = {
	"text": "Start",
	"fg": "white",
	"bg": "green",
}

STOP_BTN_CONFIG = {
	"text": "Stop",
	"fg": "white",
	"bg": "red",
}

root_ref = None
entry_ref = None
button_ref = None
start_datetime = None
stop_datetime = None
is_started = False


def main():
	log_errors(mainloop)


def mainloop():
	global start_datetime
	
	init_gui()
	recover_cached_entry()
	root_ref.mainloop()

	start_datetime = None
	wrtie_start_cache()
	
	
def recover_cached_entry():
	cached = read_start_cache()
	if cached == NULL_STR:	
		return
	global entry_ref, start_datetime, stop_datetime
	cached_subj, cached_start = cached.split(",")
	entry_ref.delete(0, tk.END)
	entry_ref.insert(0, cached_subj)
	start_datetime = dt.datetime.strptime(cached_start, DATETIME_FORMAT)
	stop_datetime = get_last_shutdown_datetime()
	write_entry()
	entry_ref.delete(0, tk.END)
	
	
def init_gui():
	global root_ref, entry_ref, button_ref
	
	root_ref = tk.Tk()
	root_ref.title(WINDOW_NAME)
	root_ref.geometry(WINDOW_GEO)
	root_ref.iconphoto(
		True,
		tk.PhotoImage(file=ICON_PATH)
	)
	
	entry_ref = tk.Entry(root_ref)
	entry_ref.bind("<Return>", unfocus_entry)
	entry_ref.bind("<Escape>", unfocus_entry)
	entry_ref.bind("<Button>", unfocus_entry)
	entry_ref.bind("<FocusIn>", on_entry_focus)
	entry_ref.bind("<FocusOut>", on_entry_unfocus)
	entry_ref.pack(
		fill="x",
		padx=MARGIN,
		pady=MARGIN,
	)
	on_entry_unfocus(None)
	
	ttk.Separator(root_ref, orient=tk.HORIZONTAL).pack(fill="x")
	
	button_ref = tk.Button(
		root_ref,
		command=toggle_button,
		**START_BTN_CONFIG
	)
	button_ref.pack(
		expand=True, 
		fill="both",
		padx=MARGIN,
		pady=MARGIN
	)
	
	
def get_last_shutdown_datetime():
	# The following bash command:
	# 	1. Pulls up the list of executed commands
	# 	2. greps all instances of "shutdown"
	# 	3. Retrieves the last instance of a shutdown
	# 	4. Removes duplicate spaces to allow cutting
	# 	5. Extracts the time and date from the string
	cmd = "last -x | grep shutdown | head -n 1 | sed -e 's,  , ,g' | cut -d' ' -f6-8"
	response = subprocess.check_output(cmd, shell=True)
	shutdown_str = f"{get_current_year()} {response.decode(CHAR_ENCODING).strip()}"
	shutdown_datetime = dt.datetime.strptime(shutdown_str, SHUTDOWN_FORMAT)
	return shutdown_datetime
	
	
def unfocus_entry(event):
	root_ref.focus_set()


def on_entry_focus(event):
	current = entry_ref.get()
	if current == ENTRY_PLACEHOLDER:
		entry_ref.delete(0, tk.END)
		entry_ref.config(
			fg=ENTRY_FOCUSED_FG,
			font=ENTRY_FOCUSED_FONT
		)
		
def on_entry_unfocus(event):
	if len(entry_ref.get()) == 0:
		entry_ref.insert(0, ENTRY_PLACEHOLDER)
		entry_ref.config(
			fg=ENTRY_UNFOCUSED_FG,
			font=ENTRY_UNFOCUSED_FONT
		)


def toggle_button():
	global is_started
	if button_ref:
		func = stop if is_started else start
		func()
		is_started = not is_started
		
		
def get_current_year():
	now = dt.datetime.now()
	year = int(now.strftime(YEAR_FORMAT))
	return year
	
		
def start():
	global start_datetime
	start_datetime = dt.datetime.now()
	wrtie_start_cache()
	button_ref.config(**STOP_BTN_CONFIG)
	entry_ref.config(state=DISABLED)
	

def stop():
	global stop_datetime, start_datetime
	stop_datetime = dt.datetime.now()
	write_entry()
	start_datetime = None
	wrtie_start_cache()
	button_ref.config(**START_BTN_CONFIG)
	entry_ref.config(state=ENABLED)
	
	
def read_start_cache():
	if not os.path.isfile(START_CACHE_PATH):
		write_start_cache()		
	with open(START_CACHE_PATH, "r") as cache:
		return cache.read()
	
			
def wrtie_start_cache():
	with open(START_CACHE_PATH, "w") as cache:
		if start_datetime is None:
			cache.write(NULL_STR)
		else:
			cache.write(f"{get_entered_text()},{start_datetime.strftime(DATETIME_FORMAT)}")
	
	
def write_entry():
	if start_datetime is None or stop_datetime is None:
		return
	with open(CSV_PATH, "a") as csv:
		subject = get_entered_text()
		start_str = start_datetime.strftime(DATETIME_FORMAT)
		stop_str = stop_datetime.strftime(DATETIME_FORMAT)
		length = int((stop_datetime - start_datetime).total_seconds() // 60)
		entry = ENTRY_FORMAT.format(
			subject,
			start_str,
			stop_str,
			length
		)
		csv.write(entry)
		

def get_entered_text():
	entered = entry_ref.get().strip()
	return NULL_STR if len(entered) == 0 or entered == ENTRY_PLACEHOLDER else entered
		
		
def log_errors(func):
	try:
		func()
	except Exception as error:
		with open(LOG_PATH, "w") as log:	
			stack = traceback.extract_tb(error.__traceback__)
			stack_trace = str(error) + "".join(stack.format())
			print(stack_trace)
			log.write(stack_trace)
			
			
if __name__ == "__main__":
	main()
	
