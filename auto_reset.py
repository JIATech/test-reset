import os
import sys
import ctypes
import pydirectinput
import time
import pyperclip

def run_as_admin():
    if sys.platform.startswith('win'):
        try:
            # Get the path of the current script
            script_path = os.path.abspath(sys.argv[0])
            
            # Run the script with admin privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)
            
            # Exit the current script
            sys.exit()
        except Exception as e:
            print(f"Failed to run as admin: {e}")

# Check if the script is running with admin privileges
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    run_as_admin()

# Copy a string to the clipboard
pyperclip.copy('/')

# Sleep for a bit
for i in range(120, 0, -1):
    print(i)
    time.sleep(1)

while True:
    # Press enter
    pydirectinput.press('enter')
    print("Pressed enter")

    # Delay before typing the word
    time.sleep(2)
    print("Waiting before typing...")

    # Type the word
    # Press down the Ctrl key
    pydirectinput.keyDown('ctrl')
    # Press the 'v' key
    pydirectinput.press('v')
    # Release the Ctrl key
    pydirectinput.keyUp('ctrl')
    word = "reset"
    for char in word:
        pydirectinput.press(char)
    print(f"Typed: {word}")

    # Press enter again
    pydirectinput.press('enter')
    print("Pressed enter again")

    # Sleep for a bit
    for i in range(120, 0, -1):
        print(i)
        time.sleep(1)
