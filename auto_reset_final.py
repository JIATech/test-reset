import os
import sys
import ctypes
import pydirectinput
import time
import pyperclip
import pygetwindow as gw
from colorama import init, Fore, Style

# Initialize colorama
init()

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
    print()
    print(f"Buscando ventana.")
    print()
    windows = gw.getAllWindows()
    matching_windows = [window for window in windows if all(keyword.lower() in window.title.lower() for keyword in keywords)]
    print()
    print(f"Se encontró {len(matching_windows)} coincidencia/s.")
    print()
    return [window.title for window in matching_windows]


def has_reset_condition(window_title, number):
    """Check if a window title matches the reset condition."""
    result = f"Level: {number} ||" in window_title  
    if result:
        print()
        print(f"Condiciones para reset se cumplen.\nLevel: {number}")
        print()
    return result

def has_master_reset_condition(window_title, number):
    """Check if a window title matches the reset condition."""
    result = f"Reset: {number} ||" in window_title  
    if result:
        print()
        print(f"Condiciones para reset se cumplen.\nReset: {number}")
        print()
    return result

def handle_master_reset(window_title):
    """Perform the reset actions."""
    print(f"Trayendo la ventana al frente.")
    window = gw.getWindowsWithTitle(window_title)[0]
    window.activate()
    pydirectinput.press('enter')
    print("Se presiona Enter")
    time.sleep(2) 
    print("Se esperan 2 segundos...")
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('v')
    pydirectinput.keyUp('ctrl')
    print("Se pega '/' para practicidad.")
    print("Se escribe 'mreset'...")
    for char in "mreset":
        pydirectinput.press(char)
    pydirectinput.press('enter')
    print("Se presiona Enter de nuevo.")

def handle_reset(window_title):
    """Perform the reset actions."""
    if not has_master_reset_condition(window_title, range(10, 51)):
        print(f"Trayendo la ventana al frente.")
        window = gw.getWindowsWithTitle(window_title)[0]
        window.activate()
        pydirectinput.press('enter')
        print("Se presiona Enter")
        time.sleep(2) 
        print("Se esperan 2 segundos...")
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('v')
        pydirectinput.keyUp('ctrl')
        print("Se pega '/' para practicidad.")
        print("Se escribe 'mreset'...")
        for char in "mreset":
            pydirectinput.press(char)
        pydirectinput.press('enter')
        print("Se presiona Enter de nuevo.")
        pydirectinput.press('enter')
        print("Se presiona Enter")
        time.sleep(2) 
        print("Se esperan 2 segundos...")
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('v')
        pydirectinput.keyUp('ctrl')
        print("Se pega '/' para practicidad.")
        print("Se escribe 'reset'...")
        for char in "reset":
            pydirectinput.press(char)
        pydirectinput.press('enter')
        print("Se presiona Enter de nuevo.")
    else:
        return handle_master_reset(window_title)


# Initialize clipboard for reset command
pyperclip.copy("/")
print()
print("Se copió '/' al clipboard porque la librería 'pydirectinput' no sabe lo que es esto: /")
print()

cycle_counter = 1

while True:
    print(f"Ciclo número {cycle_counter}...")
    print()
    for window_title in get_window_title_by_keywords(['Character', 'Level']):
        for number_level in range(380, 401):
            has_reset_condition(window_title, number_level)
            parts = window_title.split(" || ")
            level_part = next(part for part in parts if part.strip().startswith('Level'))
            print(Fore.GREEN + Style.BRIGHT + f"Nivel actual muy bajo: {level_part}." + Fore.RED + Style.BRIGHT + " Se requiere lvl 380." + Style.RESET_ALL)
            print()
            pass            
            
    # Get matching window titles and handle resets efficiently
    for window_title in get_window_title_by_keywords(['Character', 'Level']): 
        for number_level in range(380, 401):  # Adjust range as needed
            if has_reset_condition(window_title, number_level):
                print(f"Condiciones de reset encontradas. Level: {number_level}")
                print()
                print(f"Trayendo ventana al frente")
                print()
                print(f"Copiando '/' al clipboard de nuevo...")
                print(f"Por si copiaste algo sin vergüenza.")
                pyperclip.copy("/")
                handle_reset(window_title)
                break  # Move on to the next window after a reset

    # Sleep to reduce CPU usage
    time.sleep(5)  
    print()
    print("Esperando 5 segundos...")
    print()
    print()
    cycle_counter += 1
