from utility import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# only requests information
"""
ID PROMPT   |    NAME PROMPT   |    SUBMIT

SCREEN -> TREEVIEW?

"""


def populate_tree(tree, data):
    # Clear existing tree data
    tree.delete(*tree.get_children())

    # Function to recursively add dictionary items to the tree
    def add_items(node, data, parent=""):
        if isinstance(data, dict):
            for key, value in data.items():
                node_id = tree.insert(parent, "end", text=key, open=False)
                add_items(node, value, node_id)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                node_id = tree.insert(parent, "end", text=f"Item {index}", open=False)
                add_items(node, item, node_id)
        elif isinstance(data, str) and "\n" in data:
            # Split the string by '\n' and add each line as a separate node
            for line in data.split("\n"):
                tree.insert(parent, "end", text=line, open=False)
        else:
            tree.insert(parent, "end", text=str(data), open=False)

    add_items(tree, data)


def patient_info(frame,sql_connection):

    def submit_process():
        patient_id = id_var.get()
        patient_name = name_var.get()


        if patient_id == "" or patient_id == None:
            patient_id = query_id_from_name(patient_name, sql_connection)
        


        if patient_id != None:
                
            # load patient data
            # update costs into the json file
            json_data = query_patient_info_json_using_id(patient_id, sql_connection)

            if json_data == None:
                populate_tree(tree, {})
            else:
                
                # query name from ID HERE

                json_data = json.loads(json_data)
                if patient_name=="":
                    json_data["Name"] = query_name_from_id(patient_id, sql_connection)
                else:
                    json_data["Name"] = patient_name
                
                for key in json_data:
                    if type(json_data[key]) == dict:
                        costs = calculate_costs(json_data[key], sql_connection)
                        json_data[key]["Total Costs"] = costs

                populate_tree(tree, json_data)
                return
        else:
            populate_tree(tree, {})
            

        messagebox.showinfo("Error", "Seems like there was an issue. Check ID and names please.")

    id_var = tk.StringVar()
    name_var = tk.StringVar()

    # ID Label and Entry
    input_frame = tk.Frame(frame)
    input_frame.pack(anchor="center", pady=5)

    id_label = tk.Label(input_frame, text="ID: ")
    id_label.pack(side="left")
    id_entry = tk.Entry(
        input_frame,
        textvariable=id_var,
    )
    id_entry.pack(side="left", padx=10)

    # Name Label and Entry
    name_label = tk.Label(input_frame, text="Name: ")
    name_label.pack(side="left")
    name_entry = tk.Entry(input_frame, textvariable=name_var)
    name_entry.pack(side="left")

    patient_name_selected_frame = tk.Frame(frame)
    patient_message = tk.Label(
        patient_name_selected_frame, text="Patient Not Selected Yet"
    )
    patient_message.pack(anchor="center")

    style = ttk.Style(frame)
    style.configure("Treeview", rowheight=20)  # SOLUTION
    tree_frame = tk.Frame(frame)
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame)
    tree.pack(fill="both", expand=True)

    submit_entry = tk.Button(
        frame, width=30, text="Find the patient's information", command=submit_process
    )
    # submit something. Write function
    submit_entry.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    patient_info(root)
    root.mainloop()
