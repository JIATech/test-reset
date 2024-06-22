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
            print("Testing privileges...")
            script_path = os.path.abspath(sys.argv[0])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)
            sys.exit()
        except Exception as e:
            print(f"Failed to run as admin: {e}")

if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    print("Requiring admin status...")
    run_as_admin()
else:
    print("Running with admin privileges. The power is mine.")

def get_window_title_by_keywords(keywords):
    """Find window titles containing all specified keywords."""
    print(f"Searching for window.")
    windows = gw.getAllWindows()
    matching_windows = [window for window in windows if all(keyword.lower() in window.title.lower() for keyword in keywords)]
    print(f"Found {len(matching_windows)} matching window(s).")
    return [window.title for window in matching_windows]

window_titles = get_window_title_by_keywords(['Character', 'Level'])
print(f"{window_titles}")

def extract_level_reset_and_name(window_title):
    """Extracts level, reset numbers and character name from a window title."""
    character_name = window_title.split("Character : ")[1].split(" ||")[0]
    level_number = int(window_title.split("Level: ")[1].split(" ||")[0])
    reset_number = int(window_title.split("Reset: ")[1].split(" ||")[0])
    return level_number, reset_number, character_name

while True:
    window_titles = get_window_title_by_keywords(['Character', 'Level'])
    
    if window_titles:
        windows_info = {}
        for index, window_title in enumerate(window_titles):
            level, reset, character_name = extract_level_reset_and_name(window_title)
            windows_info[f'window_{index + 1}'] = {
                'title': window_title,
                'level': level,
                'reset': reset,
                'name': character_name
            }
            print(f"Window {index + 1}: Name: {character_name}, Level: {level}, Reset: {reset}")

        for i in range(1, len(window_titles)+1):
            window_info = windows_info[f'window_{i}']
            level = window_info['level']
            reset = window_info['reset']
            window_title = window_info['title']
            character_name = window_info['name']

            if 381 <= level <= 400:
                print(f"Conditions for reset are met in window_{i} for {character_name}.\nLevel: {level}")
                # realiza el reset
                try:
                    window = gw.getWindowsWithTitle(window_title)[0]
                    window.activate()

                    pydirectinput.press('enter')
                    time.sleep(0.5)

                    # Enter reset commands with keyDown/keyUp for reliability
                    pyperclip.copy("/")
                    pydirectinput.keyDown('ctrl')
                    pydirectinput.press('v')
                    pydirectinput.keyUp('ctrl')

                    for char in "reset":
                        pydirectinput.keyDown(char)
                        time.sleep(0.1)
                        pydirectinput.keyUp(char)
                    pydirectinput.press('enter')
                    pydirectinput.press('enter')
                    pydirectinput.press('enter')
                    time.sleep(0.5)
                    print("Reset completed.")
                except IndexError:
                    print(f"Error: Window '{window_title}' not found.")
                except Exception as e:
                    print(f"Error during reset: {e}")

            elif 380 <= level <= 400 and reset <= 50:
                print(f"Conditions for master reset are met in window_{i} for {character_name}.\nLevel: {level} Reset: {reset}")
                # realiza el master reset
                try:
                    window = gw.getWindowsWithTitle(window_title)[0]
                    window.activate()

                    pydirectinput.press('enter')
                    time.sleep(0.5)

                    pyperclip.copy("/")
                    pydirectinput.keyDown('ctrl')
                    pydirectinput.press('v')
                    pydirectinput.keyUp('ctrl')

                    for char in "mreset":
                        pydirectinput.keyDown(char)
                        time.sleep(0.1)
                        pydirectinput.keyUp(char)
                    pydirectinput.press('enter')
                    pydirectinput.press('enter')
                    pydirectinput.press('enter')
                    time.sleep(0.5)
                    print("Master reset completed.")
                except IndexError:
                    print(f"Error: Window '{window_title}' not found.")
                except pydirectinput.PyDirectInputException as e:
                    print(f"Error during keyboard input: {e}")
                except Exception as e:
                    print(f"Error during reset: {e}")

            else:
                print(f"Conditions for reset are not met in window_{i} for {character_name}.")
        
    else:
        print("No matching window(s) found.")
    
    time.sleep(5)  # Wait for 5 seconds before checking again