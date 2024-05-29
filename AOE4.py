import time
import keyboard
from datetime import datetime, timedelta
import tkinter as tk
from threading import Thread, Timer


def press_keys(n, key):
    keyboard.press("H")
    keyboard.release("H")

    for _ in range(n):
        keyboard.press(key)
        keyboard.release(key)

    keyboard.press("esc")
    keyboard.release("esc")


def press_keys_f(n, f, key):
    keyboard.press(f)
    keyboard.release(f)
    for _ in range(n):
        keyboard.press(key)
        keyboard.release(key)
    keyboard.press("esc")
    keyboard.release("esc")


def reset():
    global start, end
    start = datetime.now()
    end = start + timedelta(minutes=8)
    print("===已重置===", flush=True)
    text_box.insert(tk.END, "===已重置===\n")


def pause():
    global is_paused
    is_paused = not is_paused
    if is_paused:
        print("===已暂停===", flush=True)
        text_box.insert(tk.END, "===已暂停===\n")
    else:
        print("===已继续===", flush=True)
        text_box.insert(tk.END, "===已继续===\n")


def start_program():
    global start, end, is_paused
    print("===循环开始===")
    start = datetime.now()
    end = start + timedelta(minutes=8)
    is_paused = False
    while not is_paused:
        now = datetime.now()
        n = int(n_entry.get())
        s = int(s_entry.get())
        print(f"===Current time: {now.strftime('%H:%M:%S')}，执行{n}次===", flush=True)
        text_box.insert(
            tk.END, f"===Current time: {now.strftime('%H:%M:%S')}，执行{n}次===\n"
        )

        if now >= end:
            press_keys(2 * n, "Q")
        else:
            press_keys(n, "Q")

        time.sleep(s)


def start_program_thread():
    global program_thread, timer
    program_thread = Thread(target=start_program)
    program_thread.start()
    timer = Timer(20 * 60, stop_program_thread)
    timer.start()


def stop_program_thread():
    global program_thread
    if program_thread.is_alive():
        print("===线程超时，终止线程===", flush=True)
        text_box.insert(tk.END, "===线程超时，终止线程===\n")
        program_thread.do_run = False  # type: ignore


def set_preset(tc):
    n = int(n_entry.get())
    s = 59
    n_entry.delete(0, tk.END)
    n_entry.insert(tk.END, str(tc * 3))
    s_entry.delete(0, tk.END)
    s_entry.insert(tk.END, str(s))


def start_keyboard_listener():
    global listener_thread, listener_active
    listener_active = True
    print("Keyboard listener started.")
    keyboard.add_hotkey("ctrl+f2+w", lambda: press_keys_f(20, "f2", "W"))
    keyboard.add_hotkey("ctrl+f3+W", lambda: press_keys_f(20, "f3", "W"))
    keyboard.wait()


def stop_keyboard_listener():
    global listener_active
    if listener_active:
        listener_active = False
        keyboard.unhook_all_hotkeys()
        print("Keyboard listener stopped.")
        text_box.insert(tk.END, "===Keyboard listener stopped===\n")


def toggle_keyboard_listener():
    global listener_thread, listener_active
    if listener_active:
        stop_keyboard_listener()
        listener_button.config(text="Start Keyboard Listener")
    else:
        listener_thread = Thread(target=start_keyboard_listener)
        listener_thread.start()
        listener_button.config(text="Stop Keyboard Listener")


def tk_init():
    root.title("Keyboard Automation")
    root.mainloop()


root = tk.Tk()
text_box = tk.Text(
    root, height=10, width=50, bg="white", fg="black", font=("Helvetica", 10)
)
text_box.pack(pady=10)

entry_frame = tk.Frame(root, bg="lightgrey", bd=0)
entry_frame.pack(pady=10, padx=10, fill="x")

n_label = tk.Label(entry_frame, text="操作次数 (n):", bg="lightgrey")
n_label.grid(row=0, column=0, padx=5)
n_entry = tk.Entry(entry_frame, bd=0)
n_entry.grid(row=0, column=1, padx=5)
n_entry.insert(tk.END, "3")

s_label = tk.Label(entry_frame, text="操作间隔 (s):", bg="lightgrey")
s_label.grid(row=1, column=0, padx=5)
s_entry = tk.Entry(entry_frame, bd=0)
s_entry.grid(row=1, column=1, padx=5)
s_entry.insert(tk.END, "59")

button_frame = tk.Frame(root, bg="lightgrey", bd=0)
button_frame.pack(pady=5, padx=10, fill="x")

reset_button = tk.Button(button_frame, text="重置", command=reset, bg="white")
reset_button.grid(row=0, column=0, padx=5)

pause_button = tk.Button(button_frame, text="暂停/继续", command=pause, bg="white")
pause_button.grid(row=0, column=1, padx=5)

start_button = tk.Button(
    button_frame, text="开始", command=start_program_thread, bg="white"
)
start_button.grid(row=0, column=2, padx=5)

listener_button = tk.Button(
    button_frame,
    text="Start Keyboard Listener",
    command=toggle_keyboard_listener,
    bg="white",
)
listener_button.grid(row=0, column=3, padx=5)

preset_button_frame = tk.Frame(root, bg="lightgrey", bd=0)
preset_button_frame.pack(pady=5, padx=10, fill="x")

tc1_button = tk.Button(
    preset_button_frame, text="1TC", command=lambda: set_preset(1), bg="white"
)
tc1_button.grid(row=0, column=0, padx=5)

tc2_button = tk.Button(
    preset_button_frame, text="2TC", command=lambda: set_preset(2), bg="white"
)
tc2_button.grid(row=0, column=1, padx=5)

tc3_button = tk.Button(
    preset_button_frame, text="3TC", command=lambda: set_preset(3), bg="white"
)
tc3_button.grid(row=0, column=2, padx=5)

if __name__ == "__main__":
    listener_active = True
    tk_init()
