import os
import shutil
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

def sanitise_name(name:str):
    start_dot = False
    if len(name) > 0 and name[0] == '.':
        start_dot = True
        name = name[1:]

    extension_location = name.rfind('.')
    filename = name[:extension_location]
    extension = name[extension_location:]
    filename = re.sub(r'[<>:"/\\|?*.]', '', filename)

    if start_dot:
        filename = '.' + filename
    return filename + extension

def enfolden(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path): # Ignore folders
            sanitised_name = sanitise_name(filename)

            # Fix name if needed
            if sanitised_name != filename:
                sanitised_path = os.path.join(directory, sanitised_name)
                os.rename(file_path, sanitised_path)
                file_path = sanitised_path

            # Make folder
            folder_name, _ = os.path.splitext(sanitised_name) # gets (file, extension)
            folder_path = os.path.join(directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            # Move file into folder
            destination = os.path.join(folder_path, sanitised_name)
            shutil.move(file_path, destination)

def main(directory=None):
    if directory:
        # Don't open gui, just do the thing
        try:
            enfolden(directory)
        except Exception as e:
            messagebox.showerror("Error", f"{e}")
    else:
        def select_directory():
            directory = filedialog.askdirectory()
            if directory:
                dir_var.set(directory)

        def organize_files():
            directory = dir_var.get()
            if not directory:
                completed_var.set("Select a directory.")
                return

            try:
                enfolden(dir_var.get()) # Will raise exception if fail

                folder = directory[directory.rfind('/'):]
                completed_var.set(f"Completed {folder}.")
            except Exception as e:
                completed_var.set(f"Error: {e}")

        root = tk.Tk()
        root.title("Enfolden")
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(padx=10, pady=10)

        label = tk.Label(frame, text="Select Directory:")
        label.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        dir_var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=dir_var, width=50)
        entry.grid(row=1, column=0, pady=5)

        browse_button = tk.Button(frame, text="Browse", command=select_directory)
        browse_button.grid(row=1, column=1, padx=5, pady=5)

        completed_var = tk.StringVar(value="None completed yet")
        completed_label = tk.Label(frame, textvariable=completed_var)
        completed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        organize_button = tk.Button(frame, text="Enfolden", command=organize_files)
        organize_button.grid(row=3, column=0, columnspan=2, pady=10)

        root.mainloop()

dir = None
if len(sys.argv) > 1:
    dir = sys.argv[1]
main(dir)