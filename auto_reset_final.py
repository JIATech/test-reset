import os
import sys
import ctypes
import pydirectinput
import time
import pyperclip
import pygetwindow as gw


def run_as_admin():
    """Elevate script privileges if needed."""
    if sys.platform.startswith('win'):
        try:
            print("Checking admin privileges...")
            script_path = os.path.abspath(sys.argv[0])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)
            sys.exit()
        except Exception as e:
            print(f"Failed to run as admin: {e}")


if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    print("Requesting admin elevation...")
    run_as_admin()
else:
    print("Running with admin privileges.")


def get_window_title_by_keywords(keywords):
    """Find window titles containing all specified keywords."""
    print(f"Searching for windows with keywords: {keywords}...")
    windows = gw.getAllWindows()
    matching_windows = [window for window in windows if all(keyword.lower() in window.title.lower() for keyword in keywords)]
    print(f"Found {len(matching_windows)} matching windows.")
    return [window.title for window in matching_windows]


def has_reset_condition(window_title, number):
    """Check if a window title matches the reset condition."""
    result = f"Level: {number} ||" in window_title  
    if result:
        print(f"Reset condition met for Level: {number} in window: {window_title}")
    return result


def handle_reset(window_title):
    """Perform the reset actions."""
    print(f"Resetting for window: {window_title}")
    pydirectinput.press('enter')
    print("Pressed Enter")
    time.sleep(2) 
    print("Waiting 2 seconds...")
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('v')
    pydirectinput.keyUp('ctrl')
    print("Pasted '/' command")
    for char in "reset":
        pydirectinput.press(char)
    pydirectinput.press('enter')
    print("Pressed Enter again")


# Initialize clipboard for reset command
pyperclip.copy("/")
print("Copied '/' to clipboard.")

while True:
    print("Starting new loop iteration...")
    # Get matching window titles and handle resets efficiently
    for window_title in get_window_title_by_keywords(['Character', 'Level']):
        for number in range(380, 401):  # Adjust range as needed
            if has_reset_condition(window_title, number):
                handle_reset(window_title)
                break  # Move on to the next window after a reset

    # Sleep to reduce CPU usage
    time.sleep(5)  
    print("Sleeping for 5 seconds...")
