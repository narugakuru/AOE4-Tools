import select
import time
import keyboard
from datetime import datetime, timedelta
import tkinter as tk
from threading import Thread, Timer


class KeyboardAutomationApp:
    def __init__(self, root):
        self.root = root
        self.listener_active = False
        self.is_paused = False
        self.program_thread = None
        self.listener_thread = None
        self.init_ui()

    def init_ui(self):
        self.root.title("Keyboard Automation")
        self.text_box = tk.Text(
            self.root,
            height=10,
            width=50,
            bg="white",
            fg="black",
            font=("Helvetica", 10),
        )
        self.text_box.pack(pady=10)

        entry_frame = tk.Frame(self.root, bg="lightgrey", bd=0)
        entry_frame.pack(pady=10, padx=10, fill="x")

        n_label = tk.Label(entry_frame, text="操作次数 (n):", bg="lightgrey")
        n_label.grid(row=0, column=0, padx=5)
        self.n_entry = tk.Entry(entry_frame, bd=0)
        self.n_entry.grid(row=0, column=1, padx=5)
        self.n_entry.insert(tk.END, "3")

        s_label = tk.Label(entry_frame, text="操作间隔 (s):", bg="lightgrey")
        s_label.grid(row=1, column=0, padx=5)
        self.s_entry = tk.Entry(entry_frame, bd=0)
        self.s_entry.grid(row=1, column=1, padx=5)
        self.s_entry.insert(tk.END, "59")

        button_frame = tk.Frame(self.root, bg="lightgrey", bd=0)
        button_frame.pack(pady=5, padx=10, fill="x")

        reset_button = tk.Button(
            button_frame, text="重置", command=self.reset, bg="white"
        )
        reset_button.grid(row=0, column=0, padx=5)

        pause_button = tk.Button(
            button_frame, text="暂停/继续", command=self.pause, bg="white"
        )
        pause_button.grid(row=0, column=1, padx=5)

        start_button = tk.Button(
            button_frame, text="开始", command=self.start_program_thread, bg="white"
        )
        start_button.grid(row=0, column=2, padx=5)

        self.listener_button = tk.Button(
            button_frame,
            text="Start Keyboard Listener",
            command=self.toggle_keyboard_listener,
            bg="white",
        )
        self.listener_button.grid(row=0, column=3, padx=5)

        preset_button_frame = tk.Frame(self.root, bg="lightgrey", bd=0)
        preset_button_frame.pack(pady=5, padx=10, fill="x")

        tc1_button = tk.Button(
            preset_button_frame,
            text="1TC",
            command=lambda: self.set_preset(1),
            bg="white",
        )
        tc1_button.grid(row=0, column=0, padx=5)

        tc2_button = tk.Button(
            preset_button_frame,
            text="2TC",
            command=lambda: self.set_preset(2),
            bg="white",
        )
        tc2_button.grid(row=0, column=1, padx=5)

        tc3_button = tk.Button(
            preset_button_frame,
            text="3TC",
            command=lambda: self.set_preset(3),
            bg="white",
        )
        tc3_button.grid(row=0, column=2, padx=5)

    def insert_text(self, text):
        self.text_box.insert(tk.END, text)
        self.text_box.see(tk.END)

    def press_keys_f(self, n, f, key):
        keyboard.press(f)
        keyboard.release(f)
        for _ in range(n):
            keyboard.press(key)
            keyboard.release(key)
        keyboard.press("esc")
        keyboard.release("esc")
        self.insert_text(f"==={datetime.now().strftime('%H:%M:%S')}执行{n}次{key}===\n")

    def reset(self):
        self.start = datetime.now()
        self.end = self.start + timedelta(minutes=8)
        print("===已重置===", flush=True)
        self.insert_text("===已重置===\n")

    def pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            print("===已暂停===", flush=True)
            self.insert_text("===已暂停===\n")
        else:
            print("===已继续===", flush=True)
            self.insert_text("===已继续===\n")

    def start_program(self):
        print("===循环开始===")
        self.start = datetime.now()
        self.end = self.start + timedelta(minutes=8)
        self.is_paused = False
        while not self.is_paused:
            now = datetime.now()
            n = int(self.n_entry.get())
            s = int(self.s_entry.get())
            print(
                f"===Current time: {now.strftime('%H:%M:%S')}，执行{n}次===", flush=True
            )
            self.insert_text(
                f"===Current time: {now.strftime('%H:%M:%S')}，执行{n}次===\n"
            )

            if now >= self.end:
                self.press_keys_f(2 * n, "H", "Q")
            else:
                self.press_keys_f(n, "H", "Q")

            time.sleep(s)

    def start_program_thread(self):
        self.program_thread = Thread(target=self.start_program)
        self.program_thread.start()
        self.timer = Timer(20 * 60, self.stop_program_thread)
        self.timer.start()

    def stop_program_thread(self):
        if self.program_thread.is_alive():  # type: ignore
            print("===线程超时，终止线程===", flush=True)
            self.insert_text("===线程超时，终止线程===\n")
            self.program_thread.do_run = False  # type: ignore

    def set_preset(self, tc):
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(tk.END, str(tc * 3))
        self.s_entry.delete(0, tk.END)
        self.s_entry.insert(tk.END, "59")

    def start_keyboard_listener(self):
        self.listener_active = True
        print("Keyboard listener started.")
        keyboard.add_hotkey("ctrl+f2+w", lambda: self.press_keys_f(20, "f2", "W"))
        keyboard.add_hotkey("ctrl+f3+W", lambda: self.press_keys_f(20, "f3", "W"))
        keyboard.wait()

    def stop_keyboard_listener(self):
        if self.listener_active:
            self.listener_active = False
            keyboard.unhook_all_hotkeys()
            print("Keyboard listener stopped.")
            self.insert_text("===Keyboard listener stopped===\n")

    # 键盘监听线程
    def toggle_keyboard_listener(self):
        if self.listener_active:
            self.stop_keyboard_listener()
            self.listener_button.config(text="Start Keyboard Listener")
        else:
            self.listener_thread = Thread(target=self.start_keyboard_listener)
            self.listener_thread.start()
            self.listener_button.config(text="Stop Keyboard Listener")


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardAutomationApp(root)
    root.mainloop()
