import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog,messagebox, filedialog
from tkinter import *
from utility import *
import json

def setup_json_editor(root, frame):
    def add_headers(headings_lists: list):
        tree.heading('#0', text=headings_lists[0])
        for i in range(1,len(headings_lists)):
            tree.heading(f"#{i}", text=headings_lists[i])

    def write_tree_to_json():
        def tree_to_dict(node=''):
            node_dict = {}
            for child in tree.get_children(node):
                child_name = tree.item(child, 'text')
                node_dict[child_name] = tree.item(child, 'values')

                #need more values
                #we can use this to get iterating dictionary if need be. but we do not need to do so right now so don't lol

            return node_dict
        

        choice = combo.get()
        json_dir = find_file(dirlist[choice])
        tree_data = tree_to_dict('')
        type_json = type_list[choice][1:]
        
        copy_tree_data = {}
        for key in tree_data:
            copy_tree_data[key]=[]
            for element in range(len(tree_data[key])):
                copy_tree_data[key].append(type_json[element](tree_data[key][element]))

        with open(json_dir, 'w') as json_file:
            json.dump(copy_tree_data, json_file, indent=4)
            print(f"Tree structure written to {json_dir}")

    def read_data(json_dir):
        textfile = open(find_file(json_dir), "r")
        f = json.loads(textfile.read())
        
        try:
            for index, key in enumerate(f):
                tree.insert('', tk.END, iid= index, text= key,values= f[key])
        except:
            messagebox.showinfo("Error", "Already loaded")
    
    def add_data(header_list:list):
        info_list = []
        for i in header_list: 
            root.attributes('-topmost', 1)
            key = simpledialog.askstring("Input", f"{i}:", parent=root)
            root.attributes('-topmost', 0)
            info_list.append(key)
        

        tree.insert("", tk.END, text= info_list[0], values = info_list[1:])

    
    def delete_data():
        row_id = tree.focus()
        if (row_id != ""):
            tree.delete(row_id)        

    def clear_all():
        for item in tree.get_children():
            tree.delete(item)
    def update_columns(new_headers):
        global lister
        lister = new_headers
        tree.config(columns=lister[1:])
        add_headers(lister)

    def retrieve():
        choice = combo.get()
        if choice in vlist:
            tree.config(height=20)
            clear_all()
            update_columns(vlist[choice])
            read_data(dirlist[choice])
            tree.pack(padx=5, pady=5) 
        else:
            messagebox.showinfo("Information", "Please select a valid option.")



        
    

    vlist = {
        "Staff Wages": ["Roles", "Weekday ($/hour)", "Weekend ($/hour)", "Overtime Weekday ($/hour)", "Overtime Weekend ($/hour)"],
        "Staff Roles": ["Name", "Role"],
        "Medicine/Treatment Prices": ["Name", "Price"],
        "Barcode":["Code", "Medicine Name", "Quantity per scan"],
        "Name To ID":["Name", "ID"]
    }
    dirlist = {
        "Staff Wages": "staff-wages.json",
        "Staff Roles": "staff-roles.json",
        "Medicine/Treatment Prices": "medicine-treatment price.json",
        "Barcode":"barcode.json",
        "Name To ID":"name to id.json"
    }
    type_list = {
        "Staff Wages": [str,int,int,int,int],
        "Staff Roles": [str,str],
        "Medicine/Treatment Prices": [str,int],
        "Barcode":[str,str,int],
        "Name To ID":[str,str]
    }

    combo = ttk.Combobox(frame, values=[k for k in vlist], width=30)
    combo.set("Pick an Option")
    combo.pack(padx=5, pady=5)

    button = tk.Button(frame, text="Select Settings", command=retrieve)
    button.pack(padx=5, pady=5)

    tree = ttk.Treeview(frame, height=0)
# tree.pack(padx=5, pady=5)

# Create a frame for the buttons at the bottom
    button_frame = ttk.Frame(frame)
    button_frame.pack(side='bottom', pady=10)  # Pack the frame at the bottom of the parent frame

    left_spacer = ttk.Frame(button_frame, width=20)
    left_spacer.pack(side='left', fill='both', expand=True)  # An empty frame for pushing the buttons towards center

    # Place the buttons here, as shown previously

    right_spacer = ttk.Frame(button_frame, width=20)
    right_spacer.pack(side='left', fill='both', expand=True)  # An empty frame for pushing the buttons towards center

    # Place the buttons in the button_frame and use side='left' to align them horizontally

    button_delete = ttk.Button(button_frame, text="Delete Data", command=delete_data)
    button_delete.pack(side='left', padx=5)

    button_add = ttk.Button(button_frame, text="Add Data", command=lambda: add_data(lister))
    button_add.pack(side='left', padx=5)

    button_save = ttk.Button(button_frame, text="Save Record", command=write_tree_to_json)
    button_save.pack(side='left', padx=5)

    file_frame = ttk.Frame(frame)
    file_frame.pack(padx=10, pady=10, fill='x', expand=False)

    file_string = tk.StringVar()


    
    
# Usage
if __name__ == '__main__':
    root = tk.Tk()
    root.title("JSON File Editor")
    main_frame = ttk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill='both', expand=True)

    setup_json_editor(root,main_frame)

    root.mainloop()


#change to using search by file explorer
#modify (somehow) such that the UI looks at least OK
#color scheme all to white
