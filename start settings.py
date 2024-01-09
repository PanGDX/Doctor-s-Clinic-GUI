"""
run a bash file that checks if every file is in place. Also creates dummy files.

sidenote, create a function that checks for every necessary file
"""
from utility import load_and_check
from settings import *
from tkinter import ttk
import tkinter as tk

# no edits needed IF setup_json_editor runs correctly
connection = return_connection()

def on_closing():
    """Function to call when window is closing."""

    # save sql

    root.destroy()
    connection.close()

load_and_check()
if __name__ == "__main__":
    root = tk.Tk()
    root.title("JSON File Editor")
    main_frame = ttk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill="both", expand=True)

    tree = setup_json_editor(root, main_frame,connection)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

"""
Files -> patient info

"staff-log.xlsx"
"medicine-log.xlsx"
"medicine-treatment names.txt"
"price.json"
"staff-roles.json"
"staff-wages.json"


app.exe
calculation.exe

"""
