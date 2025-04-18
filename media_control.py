# Version: 2.0 Using Timer to reset counter
import pyautogui
import keyboard
from threading import Timer

# Define functions for each action
def pause_music():
    print("Pause music")
    keyboard.send("play/pause media")

def previous_song():
    print("Previous track")
    pyautogui.press('prevtrack')

def next_song():
    print("Next track")
    pyautogui.press('nexttrack')

# Global variables: counter and timer
press_counter = 0
reset_timer = None

# Reset counter and trigger corresponding function based on press count
def reset_counter():
    global press_counter, reset_timer
    if press_counter == 1:
        pause_music()
    elif press_counter == 2:
        previous_song()
    elif press_counter == 3:
        next_song()
    # Reset state
    press_counter = 0
    reset_timer = None

# Hotkey callback function
def hotkey_pressed():
    global press_counter, reset_timer
    press_counter += 1
    # Cancel existing timer if any
    if reset_timer is not None:
        reset_timer.cancel()
    # Set a short delay (e.g. 0.5 seconds), execute corresponding function if no new keypress
    reset_timer = Timer(0.5, reset_counter)
    reset_timer.start()

# Register Ctrl+Space hotkey
keyboard.add_hotkey('ctrl+space', hotkey_pressed)

print("Music control started, press Ctrl+Space to control")
keyboard.wait()  # Keep program running