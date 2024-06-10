import os
import sys
import ctypes
import pydirectinput
import time
import pyperclip
import pygetwindow as gw


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
for i in range(10, 0, -1):
    print(i)
    time.sleep(1)

while True:
    # Check window name
    def get_window_title_by_keywords(keywords):
        windows = gw.getAllWindows()
        matching_windows = [window for window in windows if all(keyword.lower() in window.title.lower() for keyword in keywords)]
        return [window.title for window in matching_windows]

    window_title = get_window_title_by_keywords(['Character', 'Level'])
    print(window_title)
    
    # check if window_title contain certain keyword then do something
    def reset_condition_in_window_title(window_title, number):
        return str(number) in window_title
        
    def reset_condition(number):
        if reset_condition_in_window_title(window_title, number):
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
            for i in range(5, 0, -1):
                print(i)
                time.sleep(1)
        else:
            print("No reset condition found")
            # Sleep for a bit
            for i in range(5, 0, -1):
                print(i)
                time.sleep(1)
            
    for number in range(380, 401):
        reset_condition(number)
