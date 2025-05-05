import pydirectinput
import os
import json
import time
import keyboard
from pynput import keyboard
import threading

stop_flag = False  # 控制是否要在下一輪停止
main_lock = threading.Lock()
action_name = "Elden_Ring_Money_1.json"
countdownTime = 10  # 倒數計時的秒數

def main():
    # 確保同一時間只有一個 main 在執行
    if not main_lock.acquire(blocking=False):
        print("已有一個 main() 正在執行，跳過此次呼叫")
        return
    
    try:
        print("開始執行 main()")
        playActions(action_name)
        print("Done")
        print("結束執行 main()")
    finally:
        main_lock.release()
    

def countdownTimer():
    print("Starting", end="", flush=True)
    for i in range(0, countdownTime):
        print(".", end="", flush=True)
        time.sleep(1)
    print("Go")

def playActions(filename):
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, 'recordings', filename)

    with open(filepath, 'r') as jsonfile:
        data = json.load(jsonfile)

        for index, action in enumerate(data):
            action_start_time = time.time()

            if action['button'] == 'Key.esc':
                break

            if action['type'] == 'keyDown':
                key = convertKey(action['button'])
                if action.get('pos'):
                    x, y = action['pos']
                    pydirectinput.moveTo(x, y)
                pydirectinput.keyDown(key)
                print(f"keyDown on {key}")
            elif action['type'] == 'keyUp':
                key = convertKey(action['button'])
                pydirectinput.keyUp(key)
                print(f"keyUp on {key}")
            elif action['type'] == 'click':
                x, y = action['pos']
                pydirectinput.moveTo(x, y)
                pydirectinput.click()
                print(f"click on ({x}, {y})")

            try:
                next_action = data[index + 1]
            except IndexError:
                break

            elapsed_time = next_action['time'] - action['time']
            elapsed_time -= (time.time() - action_start_time)
            if elapsed_time < 0:
                elapsed_time = 0
            print(f'sleeping for {elapsed_time}')
            time.sleep(elapsed_time)

def convertKey(button):
    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_l': 'alt',
        'alt_r': 'alt',
        'ctrl_l': 'ctrl',
        'ctrl_r': 'ctrl',
        'shift_l': 'shift',
        'shift_r': 'shift',
        'caps_lock': 'capslock',
        'page_down': 'pagedown',
        'page_up': 'pageup',
        'num_lock': 'numlock',
        'print_screen': 'printscreen',
        'scroll_lock': 'scrolllock',
        'enter': 'enter',
        'esc': 'esc',
        'space': 'space',
        'tab': 'tab',
        'backspace': 'backspace',
        'delete': 'delete',
        'up': 'up',
        'down': 'down',
        'left': 'left',
        'right': 'right',
    }

    cleaned_key = button.replace('Key.', '')
    return PYNPUT_SPECIAL_CASE_MAP.get(cleaned_key, cleaned_key)

def monitor_key():
    global stop_flag
    def on_press(key):
        global stop_flag
        try:
            if key.char == '`':
                print("偵測到 ` 鍵，設定為最後一輪")
                stop_flag = True
                return False  # 停止 listener
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# 啟動鍵盤監聽執行緒
threading.Thread(target=monitor_key, daemon=True).start()

if __name__ == "__main__":
    countdownTimer()
    while True:
        main()
        time.sleep(5)
        if stop_flag:
            break
