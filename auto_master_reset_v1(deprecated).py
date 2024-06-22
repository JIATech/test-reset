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
            print("Probando privilegios...")
            script_path = os.path.abspath(sys.argv[0])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)
            sys.exit()
        except Exception as e:
            print(f"Failed to run as admin: {e}")


if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    print("Requiriendo status de admin...")
    run_as_admin()
else:
    print("Corriendo con privilegios de admin. El poder el mío.")
    
def get_window_title_by_keywords(keywords):
    """Find window titles containing all specified keywords."""
    print(f"Buscando ventana.")
    windows = gw.getAllWindows()
    matching_windows = [window for window in windows if all(keyword.lower() in window.title.lower() for keyword in keywords)]
    print(f"Se encontró {len(matching_windows)} coincidencia/s.")
    return [window.title for window in matching_windows]

def get_level_number(window_title):
    """Extract the level number from the window title."""
    level_number = int(window_title.split("Level ")[1].split(" ")[0])
    return level_number

def get_reset_number(window_title):
    """Extract the reset number from the window title."""
    reset_number = int(window_title.split("Reset ")[1].split(" ")[0])
    return reset_number

def has_reset_and_master_reset_condition(level_number, reset_number):
    """Check if a window title matches the reset condition."""
    if 385 <= level_number <= 400 and 10 <= reset_number <= 50:
        print(f"Condiciones para reset se cumplen.\nLevel: {level_number}\nReset: {reset_number}")
        return True
    else:
        print(f"Condiciones para reset no se cumplen.\nLevel: {level_number}\nReset: {reset_number}")
        return False

    
def handle_master_reset(window_title):
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
        time.sleep(0.5)

    except IndexError:
        print(f"Error: Window '{window_title}' not found.")
    except pydirectinput.PyDirectInputException as e:
        print(f"Error during keyboard input: {e}")
    except Exception as e:
        print(f"Error during reset: {e}")


        
cycle_counter = 1
while True:
    print(f"Ciclo {cycle_counter}...")
    for window_title in get_window_title_by_keywords(['Character', 'Level']):
        get_level_number(window_title)
        get_reset_number(window_title)
        for level_number in range(385, 401):
            for reset_number in range(10, 50):
                if has_reset_and_master_reset_condition(level_number, reset_number):
                    print(f"Condiciones de reset encontradas. Level: {level_number}, Reset: {reset_number}")
                    print(f"Trayendo ventana al frente")
                    print(f"Copiando '/' al clipboard de nuevo...")
                    print(f"Por si copiaste algo sin vergüenza.")
                    pyperclip.copy("/")
                    handle_master_reset(window_title)

    time.sleep(5)
    print("Esperando 5 segundos...")
    cycle_counter += 1

