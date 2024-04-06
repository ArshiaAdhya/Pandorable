import tkinter as tk
import keyboard
import subprocess

class ToggleSwitch:
    def __init__(self):
        self.current_process = None
        self.current_process_name = None
        self.toggle_key = 'o'
        self.toggle_pressed = False

    def toggle(self):
        if self.current_process is None or self.current_process.poll() is not None:
            if self.current_process_name == "gaze":
                self.current_process = subprocess.Popen(["python", "nav.py"])
                self.current_process_name = "nav"
            else:
                self.current_process = subprocess.Popen(["python", "gaze.py"])
                self.current_process_name = "gaze"
        else:
            self.current_process.terminate()
            self.current_process = None

    def check_toggle(self):
        if keyboard.is_pressed(self.toggle_key):
            if not self.toggle_pressed:
                self.toggle_pressed = True
                self.toggle()
        else:
            self.toggle_pressed = False

def main():
    toggle_switch = ToggleSwitch()

    while True:
        toggle_switch.check_toggle()

if __name__ == "__main__":
    main()
