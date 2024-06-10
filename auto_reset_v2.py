import pygetwindow as gw
import psutil

def get_window_title_by_process_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            try:
                windows = gw.getWindowsWithTitle(proc.info['name'])
                return [window.title for window in windows]
            except:
                continue
    return None

print(get_window_title_by_process_name('your_process_name'))