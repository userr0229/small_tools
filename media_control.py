"""
A simple media control script that uses Ctrl + Space to control music playback.

Controls:
- Press Ctrl + Space 1 time: Play/Pause
- Press Ctrl + Space 2 times: Previous track

Requirements:
- keyboard module (pip install keyboard)
"""

import keyboard
import pyautogui
import time

# Variables to track key press time and count
last_press_time = 0
press_count = 0
def control_music():
    global last_press_time, press_count
    
    current_time = time.time()
    
    # If interval between two key presses is less than 0.5 seconds, increment counter
    if current_time - last_press_time < 0.5:
        press_count += 1
    else:
        press_count = 1  # Reset counter

    last_press_time = current_time

    if press_count == 1:
        # Single press: Pause/Play
        print("Ctrl + Space: Pause/Play music")
        # Send Play/Pause control command
        keyboard.send("play/pause media")
    elif press_count == 2:
        # Double press: Previous track
        print("Ctrl + Space: Switch to previous track")
        # Send previous track shortcut
        pyautogui.press('prevtrack')
        press_count = 0  # Reset counter

# Listen for Ctrl + Space
keyboard.add_hotkey("ctrl+space", control_music)

keyboard.wait()  # Keep program running