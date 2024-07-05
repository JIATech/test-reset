import os
import sys
import ctypes
import pydirectinput
import time
import pyperclip
import pygetwindow as gw
from colorama import Fore, Style, init

# Initialize colorama for colored output
init()

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
    print(f"{Fore.GREEN}Running with admin privileges. The power is mine.{Style.RESET_ALL}")

def get_window_title_by_keywords(keywords):
    """Find window titles containing all specified keywords."""
    print(f"{Fore.YELLOW}Searching for window.{Style.RESET_ALL}")
    windows = gw.getAllWindows()
    matching_windows = [window for window in windows if all(keyword.lower() in window.title.lower() for keyword in keywords)]
    print(f"{Fore.YELLOW}Found {len(matching_windows)} matching window(s).{Style.RESET_ALL}")
    return [window.title for window in matching_windows]

window_titles = get_window_title_by_keywords(['Level', 'Resets'])
print(f"{Fore.CYAN}{window_titles}{Style.RESET_ALL}")

def extract_level_reset_and_name(window_title):
    """Extracts level, reset numbers and character name from a window title."""
    # Remove the "MU" prefix if present
    window_title = window_title.replace("MU ", "")

    # Split the title based on the correct separators
    parts = window_title.split(" - ")
    character_name = parts[1].split(" / ")[0]
    level_number = int(parts[1].split("Level: ")[1].split(" / ")[0])
    reset_number = int(parts[1].split("Resets: ")[1].split(" / ")[0])
    character_name = character_name.replace(" ", "")
    return level_number, reset_number, character_name

window_data = extract_level_reset_and_name(window_titles[0])
print(window_data)

def info_to_show():
        windows_info = {}
        for index, window_title in enumerate(window_titles[0]):
            level, reset, character_name = extract_level_reset_and_name(window_title)
            windows_info[f'window_{index + 1}'] = {
                'title': window_title,
                'level': level,
                'reset': reset,
                'name': character_name
            }

        for i in range(1, len(window_titles[0])+1):
            window_info = windows_info[f'window_{i}']
            level = window_info['level']
            reset = window_info['reset']
            window_title = window_info['title']
            character_name = window_info['name']
        
        return level, reset, character_name

def are_we_there_yet(level, reset, character_name, i):
    """Check if a window title matches the reset condition."""
    
    conditions = {
        "mreset": lambda level, reset, _: level >= 400 and reset >= 10,
        "reset": lambda level, reset, _: level >= 400 and reset <= 10,
        "intermediate": lambda level, reset, _: level < 380 and reset < 10,
        "special_reset": lambda level, reset, character_name: character_name in ["JohnTheWiz", "JohnTheBK", "UnaElfa"] and level == 380 and reset >= 10,
        "special_mreset": lambda level, reset, character_name: character_name in ["JohnTheWiz", "JohnTheBK", "UnaElfa"] and level == 380 and reset == 10,
    }


    for condition, check in conditions.items():
        if check(level, reset, character_name):
            if condition == "special_reset":
                print(f"{Fore.GREEN}Conditions for vip reset are met in window_{i} for {character_name}.\nLevel: {level} Reset: {reset}{Style.RESET_ALL}")
                return "special_reset"
            elif condition == "special_mreset":
                print(f"{Fore.GREEN}Conditions for vip master reset are met in window_{i} for {character_name}.\nLevel: {level} Reset: {reset}{Style.RESET_ALL}")
                return "special_mreset"
            elif condition == "mreset":
                print(f"{Fore.GREEN}Conditions for master reset are met in window_{i} for {character_name}.\nLevel: {level} Reset: {reset}{Style.RESET_ALL}")
                return "mreset"
            elif condition == "reset":
                print(f"{Fore.GREEN}Conditions for reset are met in window_{i} for {character_name}.\nLevel: {level}{Style.RESET_ALL}")
                return "reset"
            elif condition == "intermediate":
                print(f"{Fore.YELLOW}Conditions not fully met for any reset in window_{i} for {character_name} (L:{level}, R:{reset}).{Style.RESET_ALL}")
                return None

    # Default case
    print(f"{Fore.YELLOW}Conditions for reset are not met in window_{i} for {character_name} (L:{level}, R:{reset}).{Style.RESET_ALL}")
    return None

def perform_reset(window_title, cmd, character_name, i):
    print_statement = lambda: f"{Fore.GREEN}{cmd.capitalize()} performed in window_{i} for {character_name}.{Style.RESET_ALL}"
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        window.activate()
        time.sleep(1)
        pydirectinput.press('enter')
        time.sleep(0.5)

        pyperclip.copy("/")
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('v')
        pydirectinput.keyUp('ctrl')

        for char in cmd:
            pydirectinput.keyDown(char)
            time.sleep(0.1)
            pydirectinput.keyUp(char)
        time.sleep(0.5)
        pydirectinput.press('enter')
        time.sleep(0.5)
        pydirectinput.keyDown('enter')
        time.sleep(1.5)
        pydirectinput.keyUp('enter')
        pydirectinput.press('enter')
        print(print_statement())
    except IndexError:
        print(f"{Fore.RED}Error: Window '{window_title}' not found.{Style.RESET_ALL}")
    except pydirectinput.PyDirectInputException as e:
        print(f"{Fore.RED}Error during keyboard input: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error during reset: {e}{Style.RESET_ALL}")

# Main Loop
while True:
    window_titles = get_window_title_by_keywords(['Level', 'Resets'])

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
            print(f"{Fore.BLUE}Window {index + 1}: Name: {character_name}, Level: {level}, Reset: {reset}{Style.RESET_ALL}")

        for i in range(1, len(window_titles) + 1):
            window_info = windows_info[f'window_{i}']
            level = window_info['level']
            reset = window_info['reset']
            window_title = window_info['title']
            character_name = window_info['name']

            try:
                cmd = are_we_there_yet(level, reset, character_name, i)
                print(f"{Style.DIM}{Fore.YELLOW}__________________________________________________{Style.RESET_ALL}")
                print(f"{cmd}")
                print(f"{Style.DIM}{Fore.YELLOW}__________________________________________________{Style.RESET_ALL}")
                if cmd:  # Ensure cmd is not None
                    if 'JohnTheWiz' in character_name:
                        # do nothing
                        pass
                    elif "reset" in cmd and 'JohnTheWiz' or 'JohnTheBK' or 'UnaElfa' not in character_name:
                        # Perform the reset
                        print(f"{Fore.GREEN}Performing a reset.{Style.RESET_ALL}")
                        perform_reset(window_title, "reset", character_name, i)
                    elif "mreset" in cmd and 'JohnTheWiz' or 'JohnTheBK' or 'UnaElfa' not in character_name:
                        # Perform the master reset
                        print(f"{Fore.GREEN}Performing a master reset.{Style.RESET_ALL}")
                        perform_reset(window_title, cmd, character_name, i)
                    elif "special_reset":
                        # Perform the special reset
                        print(f"{Fore.GREEN}Performing a special reset.{Style.RESET_ALL}")
                        perform_reset(window_title, "reset", character_name, i)
                    elif "special_mreset":
                        # Perform the special master reset
                        print(f"{Fore.GREEN}Performing a special master reset.{Style.RESET_ALL}")
                        perform_reset(window_title, "mreset", character_name, i)
                    elif "intermediate" in cmd:
                        print(f"{Fore.YELLOW}Conditions not fully met for any reset in window_{i} for {character_name} (L:{level}, R:{reset}).{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Error: Unknown command '{cmd}' for window_{i} for {character_name}.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}No valid command for window_{i} for {character_name}.{Style.RESET_ALL}")
                    print(f"{Style.DIM}{Fore.YELLOW}__________________________________________________{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}An error occurred: {e}.{Style.RESET_ALL}")
            finally:
                if 'JohnTheWiz' in character_name:
                    if level == 380 and not reset >= 10:
                        print(f"{Fore.GREEN}JohnTheWiz is at level 380. Performing a reset.{Style.RESET_ALL}")
                        perform_reset(window_title, "reset", character_name, i)
                    elif level == 400 and reset >= 10:
                        print(f"{Fore.GREEN}JohnTheWiz is at level 400 and reset 10. Performing a reset lvl400.{Style.RESET_ALL}")
                        perform_reset(window_title, "reset", character_name, i)
                    else:
                        print(f"{Fore.GREEN}JohnTheWiz is at level {level}, needs {400 - level} more levels to reset.{Style.RESET_ALL}")
                        pass
                elif 'JohnTheBK' in character_name:
                    if level == 380 and not reset >= 10:
                        print(f"{Fore.GREEN}JohnTheBK is at level 380. Performing a reset.{Style.RESET_ALL}")
                        perform_reset(window_title, "reset", character_name, i)
                    elif level == 400 and reset >= 10:
                        print(f"{Fore.GREEN}JohnTheBK is at level 400 and reset 10. Performing a reset lvl400.{Style.RESET_ALL}")
                        perform_reset(window_title, "reset", character_name, i)
                    else:
                        print(f"{Fore.GREEN}JohnTheBK is at level {level}, needs {400 - level} more levels to reset.{Style.RESET_ALL}")
                        pass
                elif 'UnaElfa' in character_name:
                    if level == 380 and not reset >= 10:
                        print(f"{Fore.GREEN}UnaElfa is at level 380. Performing a reset.{Style.RESET_ALL}")
                        perform_reset(window_title, "reset", character_name, i)
                    elif level == 400 and reset >= 10:
                        print(f"{Fore.GREEN}UnaElfa is at level 400 and reset 10. Performing a reset lvl400.{Style.RESET_ALL}")
                        perform_reset(window_title, "reset", character_name, i)
                    else:
                        print(f"{Fore.GREEN}UnaElfa is at level {level}, needs {400 - level} more levels to reset.{Style.RESET_ALL}")
                        pass
                pass

    time.sleep(5)  # Wait for 5 seconds before checking
