import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from utility import *


# TRY OUT LATER


# NOTE:
# modified to staff-roles, not reliant on staff names anymore

def has_clocked_in(connection,name):
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM Clinic.StaffLog WHERE Date = %s AND Name = %s AND (TimeOut IS NULL OR TimeOut = '') AND (Patients IS NULL OR Patients = '');"
        cursor.execute(query, (date, name))
        result = cursor.fetchone()
        return result is not None
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


def get_names(connection):
    cursor = connection.cursor()

# SQL query to retrieve unique names from the table
    query = "SELECT DISTINCT Name FROM Clinic.StaffRoles;"

    # Execute the query
    cursor.execute(query)

    # Fetch all the rows
    rows_in_dict = cursor.fetchall()

    # return the names
    output_row = [key['Name'] for key in rows_in_dict]
    return output_row 


def clockinclockout(frame, sql_connection):
    
    # loads the names from sql
    names_from_sql_row = get_names(sql_connection)
    

    # Create the main window and set its size
    input_var = tk.StringVar()

    message = tk.Message(
        frame,
        text="Names",
        width=500,
    )
    # Create a listbox for the names and set the font size
    name_listbox = tk.Listbox(
        frame, listvariable=tk.Variable(value=names_from_sql_row), width=50, height=20
    )
    name_listbox.pack(pady=20)

    # Function to handle clocking in
    def clock_in():
        # Check if a name is selected
        if not name_listbox.curselection():
            messagebox.showinfo("Clock In", "No Names Chosen")

            return
        # Get the selected name
        name = name_listbox.get(name_listbox.curselection())

        
        # code that checks if the person has clocked in on this day
        clocked_in = has_clocked_in(sql_connection,name)    # MAKE SURE TO CHECK FOR THE SAME DAY
        if clocked_in:
            messagebox.showinfo("Clocked In Already", f"{name} already clocked in")
            return
        
        # Get the current date and time
        now = datetime.now()
        date = now.strftime("%d/%m/%Y")

        if now.minute < 10:
            time = f"{now.hour}:0{now.minute}"
        else:
            time = f"{now.hour}:{now.minute}"
        
        # Show a message box
        messagebox.showinfo("Clock In", f"{name} Logged in at: {date} {time}")

        # Write to the sql
        cursor = sql_connection.cursor()
        # SQL query to insert data
        query = "INSERT INTO Clinic.StaffLog (Date, Name, TimeIn) VALUES (%s, %s, %s);"

        # Execute the query
        cursor.execute(query, 
                       [date, name, time])
        sql_connection.commit()
        print("Data inserted successfully.")




    # Function to handle clocking out
    def clock_out():
        patients_treated = input_var.get()

        # Check if a name is selected
        if not name_listbox.curselection():
            messagebox.showinfo("Clock Out", "No Names Chosen")
            return
        # check if number of treated patients is filled
        if not patients_treated:
            messagebox.showinfo(
                "Clock Out", "Missing Patient Input"
            )
            return

        # check if input field is an integer
        try:
            int(patients_treated)
        except:
            messagebox.showinfo("Clock Out", "Not a number")
            return

        # Get the selected name
        name = name_listbox.get(name_listbox.curselection())

        # Get the current date and time
        now = datetime.now()
        date = now.strftime("%d/%m/%Y")
        if now.minute < 10:
            time = f"{now.hour}:0{now.minute}"
        else:
            time = f"{now.hour}:{now.minute}"
        
        
        # Check if the user has clocked in
        # Update the clock out time
        # Show a message box
            
        cursor = sql_connection.cursor()
        check_query = "SELECT * FROM Clinic.StaffLog WHERE Date = %s AND Name = %s AND (TimeOut IS NULL OR TimeOut = '') AND (Patients IS NULL OR Patients = '');"
        cursor.execute(check_query, (date, name))
        if cursor.fetchone() is None:
            messagebox.showinfo("Clock Out", f"{name} already logged out")
            print(f"No clock-in record found for {name} today.")
            return 
        
        update_query = "UPDATE Clinic.StaffLog SET TimeOut = %s, Patients = %s WHERE Date = %s AND Name = %s;"
        cursor.execute(update_query, (time, patients_treated, date, name))
        sql_connection.commit()

        messagebox.showinfo("Clock Out", f"{name} logged out at: {date} {time}")

        return
        # If the user has not clocked in, show a message box

    # Create the clock in button
    clock_in_button = tk.Button(
        frame, text="Clock In", command=clock_in, width=8, height=1
    )
    clock_in_button.pack()

    # Create the clock out button
    clock_out_button = tk.Button(
        frame, text="Clock Out", command=clock_out, width=8, height=1
    )
    clock_out_button.pack(pady=20)

    message = tk.Message(
        frame,
        text="Input the number of patients:",
        width=500,
        justify="center",
    )
    message.pack(pady=10)

    entry = tk.Entry(frame, textvariable=input_var, width=50)
    entry.pack(pady=20)

    message = tk.Message(
        frame,
        text="To edit the name list, go to settings and choose 'Staff Names'",
        width=500,
    )
    message.pack()

    
    # Start the main loop


if __name__ == "__main__":
    ws = tk.Tk()
    clockinclockout(ws, return_connection())
    ws.mainloop()  # This line starts the Tkinter event loop
