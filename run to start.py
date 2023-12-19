"""
run a bash file that checks if every file is in place. Also creates dummy files.

sidenote, create a function that checks for every necessary file
"""
from utility import load_and_check
from settings import setup_json_editor
from tkinter import ttk
import tkinter as tk


load_and_check()
if __name__ == '__main__':
    root = tk.Tk()
    root.title("JSON File Editor")
    main_frame = ttk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill='both', expand=True)

    setup_json_editor(root,main_frame)

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