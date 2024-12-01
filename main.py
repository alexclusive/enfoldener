import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import re

def sanitize_name(name:str):
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

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        dir_var.set(directory)

def organize_files():
    directory = dir_var.get()
    if not directory:
        messagebox.showerror("Error", "Please select a directory first.")
        return
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            # Skip directories, process only files
            if os.path.isfile(file_path):
                # Sanitize the file name
                sanitized_name = sanitize_name(filename)

                # Rename the file if necessary
                if sanitized_name != filename:
                    sanitized_path = os.path.join(directory, sanitized_name)
                    os.rename(file_path, sanitized_path)
                    file_path = sanitized_path

                # Use the sanitized name (without extension) to create the folder
                folder_name = os.path.splitext(sanitized_name)[0]
                folder_path = os.path.join(directory, folder_name)

                # Create the folder if it doesn't exist
                os.makedirs(folder_path, exist_ok=True)

                # Move the file into the newly created folder
                destination_path = os.path.join(folder_path, sanitized_name)
                shutil.move(file_path, destination_path)

        # messagebox.showinfo("Success", "Files have been organized successfully!")
        folder = directory[directory.rfind('/'):]
        completed_variable.set("Completed " + folder)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Organize Files by Folder")

# Create and place widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

dir_var = tk.StringVar()

label = tk.Label(frame, text="Selected Directory:")
label.grid(row=0, column=0, sticky="w", pady=5)

entry = tk.Entry(frame, textvariable=dir_var, width=50, state="readonly")
entry.grid(row=1, column=0, pady=5)

browse_button = tk.Button(frame, text="Browse", command=select_directory)
browse_button.grid(row=1, column=1, padx=5, pady=5)

completed_variable = tk.StringVar(value="None completed yet")
completed_label = tk.Label(frame, textvariable=completed_variable)
completed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

organize_button = tk.Button(frame, text="Enfolden", command=organize_files)
organize_button.grid(row=3, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()