"""
A simple media control script that uses Ctrl + Space to control music playback.

Controls:
- Press Ctrl + Space 1 time: Play/Pause
- Press Ctrl + Space 2 times: Previous track
- Press Ctrl + Space 3 times: Next track

Requirements:
- keyboard module (pip install keyboard)
"""


import keyboard
import time

# Counter and timer for hotkey actions
counter = 0
start_time = None

def handle_music_action(action):
    if action == "pause":
        print("Pause music")
        # Insert code to pause music here
    elif action == "previous":
        print("Previous track")
        # Insert code to play previous track here
    elif action == "next":
        print("Next track")
        # Insert code to play next track here

def on_ctrl_space():
    global counter, start_time
    if start_time is None:
        start_time = time.time()
    counter += 1

# Set up hotkey listener
keyboard.add_hotkey("ctrl+space", on_ctrl_space)

try:
    print("Press Ctrl + Space to control music (1x pause, 2x previous, 3x next)")
    while True:
        if start_time and time.time() - start_time > 0.5:  # Set 0.5 second detection window
            if counter == 1:
                handle_music_action("pause")
            elif counter == 2:
                handle_music_action("previous")
            elif counter == 3:
                handle_music_action("next")
            counter = 0
            start_time = None
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program stopped")