import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from tkinter import *
from utility import *



# write a function that reads from sql to json
# then another function that updates back once program shuts down



#Fill in info
name_to_table_name = {"Staff Wages":"RolesPayment",
    "Staff Roles":"StaffRoles",
    "Medicine/Treatment Prices":"MedicineTreatmentPrices",
    "Barcode":"Barcode",
    "Name To ID":"NameToID",}

expected_columns ={"Staff Wages":["Roles", "WeekdayDollarPerHour", "WeekendDollarPerHour", "OvertimeWeekdayDollarPerHour", "OvertimeWeekendDollarPerHour"],
    "Staff Roles":["Name", "Role"],
    "Medicine/Treatment Prices":["Name", "Price", "CostPrice"],
    "Barcode":["Code", "MedicineName", "QuantityPerScan"],
    "Name To ID":["Name", "ID"]}

def is_treeview_empty(tree):
    """
    Check if a ttk.Treeview widget is empty.

    Parameters:
    tree (ttk.Treeview): The Treeview widget to check.

    Returns:
    bool: True if the Treeview is empty, False otherwise.
    """
    return not tree.get_children()

# Example usage:
# Assuming 'tree' is your ttk.Treeview widget
# empty = is_treeview_empty(tree)
# print("Treeview is empty:", empty)

def identify_tree_and_save(tree, connection):
    current_columns = tree.cget('columns')

    previous_settings = ""
    for key in expected_columns:
        if set(expected_columns[key]) == set(current_columns):
            previous_settings = key
            break
    print("Previous settings:")
    print(previous_settings)

    if previous_settings != "" and not is_treeview_empty(tree):
        table_name = name_to_table_name[previous_settings]

        tree_data = [tree.item(item)['values'] for item in tree.get_children()]

        # Create a cursor object
        cursor = connection.cursor()

        # Delete existing data in the table
        cursor.execute(f"DELETE FROM {table_name}")

        # Assuming we know the structure of the table and treeview
        # Example: INSERT INTO table_name (col1, col2, col3) VALUES (%s, %s, %s)
        insert_query = f"INSERT INTO {table_name} VALUES (" + ", ".join(["%s"] * len(tree_data[0])) + ")"

        # Insert new data into the table
        cursor.executemany(insert_query, tree_data)

        # Commit the changes to the database
        connection.commit()

        # Close the cursor
        cursor.close()
        print(f"Table {table_name} updated successfully.")
    # delete sql table
    # save tree to sql





def setup_json_editor(root, frame,sql_connection):

    def add_data():
        info_list = [""]
        column_names = tree["columns"]
        for i in column_names:
            root.attributes("-topmost", 1)
            key = simpledialog.askstring("Input", f"{i}:", parent=root)
            root.attributes("-topmost", 0)
            info_list.append(key)

        tree.insert("", tk.END, text=info_list[0], values=info_list[1:])

    def delete_data():
        row_id = tree.focus()
        if row_id != "":
            tree.delete(row_id)





    def load_all_info_into_tree(table_name:str, tree, connection):
        """
        clear the tree and then
        takes in the table name and updates the tree. 
        """
        def clear_all():
            for item in tree.get_children():
                tree.delete(item)
        
        clear_all()

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        cursor.close()

        # Update the Treeview columns
        tree['columns'] = column_names
        tree.column("#0", width=0, stretch=tk.NO)  # Hiding the default column
        for col in column_names:
            tree.column(col, anchor=tk.CENTER)
            tree.heading(col, text=col)

        # Insert new data into the Treeview
        
        

        for row in rows:
            values_list = []
            for key in row:
                values_list.append(row[key])
            print(row)
            print(type(row))
            tree.insert('', 'end', values=values_list)
        print(f"Inserted from {table_name}!")
    

    def retrieve():
        identify_tree_and_save(tree,sql_connection)
        choice = combo.get()
        if choice in name_to_table_name:
            
            tree.config(height=20)
            

            #name_to_table_name[choice] is the name of the table 
            load_all_info_into_tree(name_to_table_name[choice],tree,sql_connection)
            
            tree.pack(padx=5, pady=5)
        else:
            messagebox.showinfo("Information", "Please select a valid option.")


    
    combo = ttk.Combobox(frame, values=[k for k in name_to_table_name], width=30)
    combo.set("Pick an Option")
    combo.pack(padx=5, pady=5)

    button = tk.Button(frame, text="Select Settings", command=retrieve)
    button.pack(padx=5, pady=5)

    tree = ttk.Treeview(frame, height=0)
    # tree.pack(padx=5, pady=5)

    # Create a frame for the buttons at the bottom
    button_frame = ttk.Frame(frame)
    button_frame.pack(
        side="bottom", pady=10
    )  # Pack the frame at the bottom of the parent frame

    left_spacer = ttk.Frame(button_frame, width=20)
    left_spacer.pack(
        side="left", fill="both", expand=True
    )  # An empty frame for pushing the buttons towards center

    # Place the buttons here, as shown previously

    right_spacer = ttk.Frame(button_frame, width=20)
    right_spacer.pack(
        side="left", fill="both", expand=True
    )  # An empty frame for pushing the buttons towards center

    # Place the buttons in the button_frame and use side='left' to align them horizontally

    button_delete = ttk.Button(button_frame, text="Delete Data", command=delete_data)
    button_delete.pack(side="left", padx=5)

    button_add = ttk.Button(
        button_frame, text="Add Data", command=lambda: add_data()
    )
    button_add.pack(side="left", padx=5)


    file_frame = ttk.Frame(frame)
    file_frame.pack(padx=10, pady=10, fill="x", expand=False)

    return tree


# Usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("JSON File Editor")
    main_frame = ttk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill="both", expand=True)

    setup_json_editor(root, main_frame, return_connection())

    root.mainloop()


# change to using search by file explorer
# modify (somehow) such that the UI looks at least OK
# color scheme all to white
