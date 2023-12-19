from utility import *
import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook
import sys,asyncio
from threading import Thread
"""
Leave empty: Add/subtract by clinic
ID PROMPT   |    NAME PROMPT   |    NEW PATIENT (TICK)
SUBMIT 


MEDICINE LISTBOX
ADD/SUBTRACT
"""

#Scan:
    # immediately call:
    # ID, Name, and submit immediately want to be seaparte
    #

def medicine(frame):
    create_medicine_sheet()

    async def read_stdin():
        loop = asyncio.get_running_loop()
        while True:
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if line:
                await qr_code_submit(line.strip())
            else:
                break

    async def qr_code_submit(key_input):
    #key input is the number of the medicine/treatment (identifier)
        patient_id = id_var.get()
        medicine_name = qrcode_json[key_input][0]
        quantity_of_med = qrcode_json[key_input][1]


        if patient_id=="" or patient_id==None:
            patient_id=0
        try:
            patient_id = int(patient_id)
        except:
            messagebox.showinfo(
                    "Error", f"Patient ID must be a number"
                )
            return 
        
        patient_name = name_var.get()
        doctor_note = doctor_note_textbox.get('1.0', 'end-1c')  
        

        if patient_id == 0 and patient_name=="":
            return

        # processing for patient
        if patient_id == 0:
            if patient_name != "":
                # attempt to assign patient ID based on patient name
                try:
                    patient_id = name_to_id_json[patient_name]
                except:
                    messagebox.showinfo(
                        "Error", f"No patient with that ID"
                    )
                    return 
        else:
            # attempt to assign patient name based on ID
            if patient_name=="":
                patient_name=get_name_from_json(patient_id)

        # assign new patient name to ID
        log_name_to_id(patient_name, patient_id)
        


        
            # update for patient X
        patient_message.config(text=f"Patient Name:{patient_name}")

        save_to_patient_file(patient_id, 
                            medicine_or_treatment=medicine_name,
                            quantity=int(quantity_of_med),
                            doctor_note=doctor_note)
        
        modify_medicine_log(medicine_name, int(quantity_of_med) * -1)

    def start_asyncio_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
    def create_popup_clinic(callback):
        def on_submit():
            callback(add_var.get(), subtract_var.get())
            popup.destroy()
            
        popup = tk.Toplevel(frame)
        popup.geometry("200x150")
        popup.title("Option")    


        chk1 = tk.Checkbutton(popup, text="Add to stock", variable=add_var)
        chk1.pack()
        chk2 = tk.Checkbutton(popup, text="Remove from stock", variable=subtract_var)
        chk2.pack()     

        close_button = tk.Button(popup, text="Submit", command=on_submit)
        close_button.pack()   

    def submit_process():
        patient_id = id_var.get()
        if patient_id=="" or patient_id==None:
            patient_id=0
        try:
            patient_id = int(patient_id)
        except:
            messagebox.showinfo(
                    "Error", f"Patient ID must be a number"
                )
            return 
        
        patient_name = name_var.get()
        quantity_of_med = quantity_var.get()
        doctor_note = doctor_note_textbox.get('1.0', 'end-1c')            

        if not name_listbox.curselection():
            messagebox.showinfo(
                    "Error", f"Did not select any medicine/treatment option yet"
                )
            return
        else:
            medicine_name = name_listbox.get(name_listbox.curselection())


        def handle_clinic_options(add_option, subtract_option):
            if add_option and not subtract_option:
                modify_medicine_log(medicine_name, int(quantity_of_med) * 1)
                
            elif not add_option and subtract_option:
                modify_medicine_log(medicine_name, int(quantity_of_med) * -1)
                
            else:
                messagebox.showinfo("Error", "Invalid Option")
                
        if (patient_id == 0) and (patient_name==""):
            #clinic add/subtract
            create_popup_clinic(handle_clinic_options)
            return 



        # processing for patient
        if patient_id == 0:
            if patient_name != "":
                # attempt to assign patient ID based on patient name
                try:
                    patient_id = name_to_id_json[patient_name]
                except:
                    messagebox.showinfo(
                        "Error", f"No patient with that ID"
                    )
                    return 
        else:
            # attempt to assign patient name based on ID
            if patient_name=="":
                patient_name=get_name_from_json(patient_id)
        
            # assign new patient name to ID
        log_name_to_id(patient_name, patient_id)
        


        if patient_id:
            # update for patient X
            patient_message.config(text=f"Patient Name:{patient_name}")

            save_to_patient_file(patient_id, 
                                medicine_or_treatment=medicine_name,
                                quantity=int(quantity_of_med),
                                doctor_note=doctor_note)
            
            modify_medicine_log(medicine_name, int(quantity_of_med) * -1)




    loop = asyncio.new_event_loop()
    t = Thread(target=start_asyncio_loop, args=(loop,), daemon=True)
    t.start()

    asyncio.run_coroutine_threadsafe(read_stdin(), loop)
    # loads the file of all the names
    medicine_price_json = json_loading('medicine-treatment price.json')
    name_to_id_json = json_loading('name to id.json')
    qrcode_json = json_loading('barcode.json')


    medicine_name = []
    for key in medicine_price_json:
        medicine_name.append(key)


    # Load or create the workbook
    log_location = find_file('medicine-log.xlsx')
    remove_blank_rows(log_location)
    workbook = load_workbook(filename=log_location)


    # Set global var tk
    id_var = tk.StringVar()
    name_var = tk.StringVar()
    quantity_var = tk.IntVar()
    add_var = tk.BooleanVar()
    subtract_var = tk.BooleanVar()

    top_message = tk.Label(frame, text="Leave Empty/Unchanged = Add/Subtract by clinic.")
    top_message.pack(anchor='center', pady = 5)

    # ID Label and Entry
    input_frame = tk.Frame(frame)
    input_frame.pack(anchor='center', pady=5)
    
    id_label = tk.Label(input_frame, text="ID: ")
    id_label.pack(side='left')
    id_entry = tk.Entry(input_frame, textvariable=id_var, )
    id_entry.pack(side='left',padx=10)

    # Name Label and Entry
    name_label = tk.Label(input_frame, text="Name: ")
    name_label.pack(side='left')
    name_entry = tk.Entry(input_frame, textvariable=name_var)
    name_entry.pack(side='left')

    patient_name_selected_frame = tk.Frame(frame)
    patient_message = tk.Label(patient_name_selected_frame, 
                               text="Patient Not Selected Yet")
    patient_message.pack(anchor='center')

    # New Patient Checkbox
    new_patient_frame = tk.Frame(frame)
    new_patient_frame.pack(anchor='center', pady=5)
    new_patient_label = tk.Label(new_patient_frame, text="New Patient? ")
    new_patient_label.pack(side='left')
    

    submit_entry = tk.Button(frame, width=30, text = "Submit/Update the information", command= submit_process )
    #submit something. Write function
    submit_entry.pack(pady=20)

    # Create a listbox 
    message = tk.Message(
        frame,
        text ="Medicine/Treatment Options",
        width=500,
    )
    message.pack()
    name_listbox = tk.Listbox(
        frame, listvariable=tk.Variable(value=medicine_name), width=50, height=20
    )
    name_listbox.pack(pady=10)

    # Create entry for number of medicine/treatment done
    quantity_frame = tk.Frame(frame)
    quantity_frame.pack(anchor='center', pady=5)
    quantity_label = tk.Label(quantity_frame, text="Quantity: ")
    quantity_label.pack(side='left')
    quantity_entry = tk.Entry(quantity_frame, textvariable=quantity_var)
    quantity_entry.pack(side='left')


    # Doctor's note to append
    message = tk.Message(
        frame,
        text ="Doctor's Note",
        width=500,
    )
    message.pack()
    doctor_note_textbox = tk.Text(frame, height=5, width=50)
    doctor_note_textbox.pack()
    #doctor_note_textbox.get()

    return loop,t




if __name__ == '__main__':
    # Set up the asyncio event loop

    

    # Set up the tkinter UI
    root = tk.Tk()
    root.geometry("1000x700")
    medicine(root)

    # Schedule the asyncio read_stdin task in the asyncio loop
    

    # Start the Tkinter main loop
    root.mainloop()

    # Once window closes, you can stop the asyncio loop
    # loop.call_soon_threadsafe(loop.stop)
    # t.join()

#Info collected:




    # Start the main loop
