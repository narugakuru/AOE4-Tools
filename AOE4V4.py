import time
import keyboard
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from threading import Thread
import queue


class KeyboardAutomationApp:
    def __init__(self, root):
        self.root = root
        self.listener_active = False
        self.is_paused = False
        self.program_thread = None
        self.listener_thread = None
        self.queue = queue.Queue()
        self.init_ui()

    def init_ui(self):
        self.root.title("Keyboard Automation")
        self.root.geometry("500x500")
        self.root.configure(bg="lightgrey")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 10), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 10), background="lightgrey")
        self.style.configure("TEntry", font=("Helvetica", 10), padding=5)
        # 文本框
        self.text_box = tk.Text(
            self.root,
            height=10,
            width=50,
            bg="white",
            fg="black",
            font=("Helvetica", 10),
        )
        # 水平居中
        self.text_box.pack(fill=tk.X)

        entry_frame = ttk.Frame(root)
        entry_frame.pack(pady=20)

        n_label = ttk.Label(entry_frame, text="操作次数 (n):")
        n_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.n_entry = ttk.Entry(entry_frame)
        self.n_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.n_entry.insert(tk.END, "3")

        s_label = ttk.Label(entry_frame, text="操作间隔 (s):")
        s_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.s_entry = ttk.Entry(entry_frame)
        self.s_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.s_entry.insert(tk.END, "59")

        button_frame = tk.Frame(self.root, bg="lightgrey")
        button_frame.pack(pady=5, padx=10, fill="x")

        reset_button = ttk.Button(button_frame, text="重置", command=self.reset)
        reset_button.grid(row=1, column=0, padx=5, pady=5)

        pause_button = ttk.Button(button_frame, text="暂停/继续", command=self.pause)
        pause_button.grid(row=1, column=1, padx=5, pady=5)

        start_button = ttk.Button(
            button_frame, text="开始", command=self.start_program_thread
        )
        start_button.grid(row=1, column=2, padx=5, pady=5)

        self.listener_button = ttk.Button(
            button_frame,
            text="Start Keyboard Listener",
            command=self.toggle_keyboard_listener,
        )
        self.listener_button.grid(row=0, column=1, padx=5, pady=5)

        preset_button_frame = tk.Frame(root, bg="lightgrey")
        preset_button_frame.pack(pady=5, padx=10, fill="x")

        # TC按钮
        num_preset_buttons = 3
        button_width = 12
        for i in range(num_preset_buttons):
            button = ttk.Button(
                preset_button_frame,
                text=f"{i+1}TC",
                width=button_width,
                command=lambda x=i + 1: self.set_preset(x),
            )
            button.grid(row=0, column=i, padx=5, pady=5)

    def process_queue(self):
        try:
            while True:
                text = self.queue.get_nowait()
                self.insert_text(text)
        except queue.Empty:
            self.root.after(100, self.process_queue)

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
        self.queue.put(f"==={datetime.now().strftime('%H:%M:%S')}执行{n}次{key}===\n")

    def reset(self):
        self.start = datetime.now()
        self.end = self.start + timedelta(minutes=8)
        print("===已重置===", flush=True)
        self.queue.put("===已重置===\n")

    def pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            print("===已暂停===", flush=True)
            self.queue.put("===已暂停===\n")
        else:
            print("===已继续===", flush=True)
            self.queue.put("===已继续===\n")

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
            self.queue.put(
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
            self.queue.put("===Keyboard listener stopped===\n")

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
