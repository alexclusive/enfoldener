Thank you ChatGPT :)

# Steps to Add the Script to Right-Click Menu
## Update Your Python Script
Modify your script so it accepts a directory as a command-line argument. For example:
```python
import sys
def tasks(default_dir):
	if default_dir:
		# Do task for when opened with context menu
	else:
		# Do task for when not opened with context menu

directory = None
if len(sys.argv) > 1:
	directory = sys.argv[1] # can also os.getcwd() for current working directory
tasks(directory)
```
This script allows you to pass a directory as an argument, and it will prefill the GUI with that directory.

## Create a Batch File To make the script executable from the context menu, create a batch file to run the Python script:
- Save the following as `Example.bat` (or any name you'd like):
```bat
@echo off
pythonw "C:\path\to\your\script.py" "%~1"
```
- Replace `C:\path\to\your\script.py` with the full path to your Python script.
    - `pythonw` runs the Python script without opening a terminal window.
    - `%~1` passes the path of the right-clicked directory to the script.

## Add the Batch File to the Context Menu
Add an entry to the Windows Registry for the right-click context menu:

- Press Windows + R, type `regedit`, and press Enter.
- Navigate to the following location:
```mathematica
HKEY_CLASSES_ROOT\Directory\shell
```
- Create a new key under `shell`:
    - Right-click `shell > New > Key`.
    - Name it `Example...`.
- Create a subkey under the new key:
    - Right-click `Example... > New > Key`.
    - Name it `command`.
- Set the `(Default)` value of the `command` key:
    - Double-click `(Default)` in the `command` key.
    - Set its value to:
```perl
"C:\path\to\Example.bat" "%1"
```
Replace `C:\path\to\Example.bat` with the full path to your batch file.

## Test the Context Menu
- Right-click on a folder in File Explorer.
- You should see the option "YTDownloader here...".
- Clicking it should open your script's GUI with the directory prefilled.

## Optional Enhancements
- Icon for the Context Menu Entry: Add an icon by creating a `String Value` named `Icon` in the `Example...` key and setting its value to:
```perl
"C:\path\to\your\icon.ico"
```
Replace `C:\path\to\your\icon.ico` with the full path to your icon file.

- Error Logging: Modify your Python script to log any errors in case the context menu action fails.

This approach will let you seamlessly integrate your script with Windows Explorer!