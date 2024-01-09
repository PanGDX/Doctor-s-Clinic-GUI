import tkinter as tk
import tkinter.ttk as ttk
from clockinclockout import clockinclockout
from utility import *
from settings import *
from sendmessage import create_message_box_page
from medicine import medicine
from patient_info_request import patient_info
import threading,socket


# remaining things to do: test async with actual barcode scanner
# test inputs

# Add write_to_tree when on_closing and when switching



# SHOULD WORK ONCE EVERYTHING ELSE OK






# socket stuff


def handle_client(conn, addr):
    print(f"Connection from {addr}")
    data = b''
    while True:
        part = conn.recv(1024)
        data += part
        if len(part) < 1024:
            # No more data, or less than buffer size data is received
            break
    if data:
        data_decoded = data.decode("utf-8")
        data_list = data_decoded.split("\n")
        print(data_list)

        computer_type = open("computer name.txt","r")
        computer_name = computer_type.read()
        if data_list[0] == computer_name:
            messagebox.showinfo("Message", "\n".join(data_list[1:]))  # Decode the binary data to a string
    else:
        print("No data received.")

def start_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 65432))
    #0.0.0.0 listens to all available networks
    server.listen()
    print("Server listening...")

    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()


threading.Thread(target=start_server,daemon=True).start()












# gui stuff


def check_unclocked_out():
    """
    False = all clocked out

    Else return list of not yet clocked out
    """
    cursor = connection.cursor()

    # SQL query to check for entries without clock-out
    query = "SELECT Name FROM StaffLog WHERE Date = %s AND TimeOut IS NULL;"

    # Execute the query
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    cursor.execute(query, (date,))  

    # Fetch the result
    results = cursor.fetchall()

    if results:
        return results
    else:
        return False
def on_closing():
    try:
        """Function to call when window is closing."""
        #update

        #identify_tree_and_save(tree,connection)
        loop.call_soon_threadsafe(loop.stop)
        t.join()

        # check if somebody did not log out yet
        results_clocked_out = check_unclocked_out()
        if results_clocked_out != False:
            name_string = " ".join(results_clocked_out)
            messagebox.showinfo("Clock Out", f"Did not all clock out yet:\n{name_string}")
        else:
            ws.destroy()
            connection.close()
    except Exception as e:
        print(e)
        ws.destroy()
        connection.close()
   
        


# Create the main window
ws = tk.Tk()
ws.geometry("1000x700")
ws.title("Notebook")


# Create a Notebook widget
notebook = ttk.Notebook(ws)



# Create four frames
staff_frame = ttk.Frame(notebook)
medicine_frame = ttk.Frame(notebook)
patient_info_frame = ttk.Frame(notebook)
message_box_frame = ttk.Frame(notebook)
#settings_frame = ttk.Frame(notebook)

# Add a label to each frame

connection = return_connection()



#hmm unsure
try:
    clockinclockout(staff_frame, connection)
    #tree = setup_json_editor(ws, settings_frame, connection)
    loop, t = medicine(medicine_frame, connection)
    patient_info(patient_info_frame, connection)
    create_message_box_page(message_box_frame)
except Exception as e:
    messagebox.showinfo("Error", f"Error: {e}")
# Pack the frames

staff_frame.pack(fill="both", expand=True)
patient_info_frame.pack(fill="both", expand=True)
medicine_frame.pack(fill="both", expand=True)
message_box_frame.pack(fill="both", expand=True)
#settings_frame.pack(fill="both", expand=True)

# Add frames to the notebook
notebook.add(staff_frame, text="  Staff Login  ")
notebook.add(medicine_frame, text="  Medicine and Treatment Logging  ")  # similar to staff login
notebook.add(patient_info_frame, text="  Search Patient Information  ")  # canvas?
notebook.add(message_box_frame, text="  Message To Other Computers  ")
#notebook.add(settings_frame, text="  Settings  ")  # treeview
notebook.pack(padx=10, pady=10, expand=True, fill="both")

# Run the main event loop
ws.protocol("WM_DELETE_WINDOW", on_closing)
ws.mainloop()
