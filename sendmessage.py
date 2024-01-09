import tkinter as tk
from tkinter import ttk
import socket
from utility import *


# no edits needed



def submit_message(computer_choice, text_choice):
    server_addr_list = find_open_ports()
    server_port = 65432
    strings = f"{computer_choice}\n{text_choice}"
    strings = strings.encode()
    print(get_local_ip())

    if server_addr_list != []: 
        for server_addr in server_addr_list:
            if server_addr != get_local_ip():
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((server_addr, server_port))
                    s.sendall(strings)

def create_message_box_page(frame):
    with open("computer name.txt", "r") as file:
        computer_type = file.read()

    text_message= tk.Message(frame, text=f"Computer name: {computer_type}", width= 100)
    text_message.pack(pady=5)

    text_box = tk.Text(frame, height=5, width=50)
    text_box.pack(pady=5)

    # Create a Combobox
    computer_options = ["Front Computer", "Upper Computer", "Inner Computer"]
    combobox = ttk.Combobox(frame, values=computer_options, state='readonly')
    combobox.set("Select Computer")  # Set the default value
    combobox.pack(pady=5)

    submit_button = tk.Button(frame, text="Submit", command=lambda: submit_message(combobox.get(), text_box.get("1.0", "end-1c")))
    submit_button.pack(pady=5)

    

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Tkinter Page")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)
    create_message_box_page(frame)
    root.mainloop()
