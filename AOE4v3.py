import time
import keyboard
from datetime import datetime, timedelta
import tkinter as tk
from threading import Thread, Timer
import queue
import os


class KeyboardAutomationApp:
    def __init__(self, root):
        self.root = root
        self.listener_active = False
        self.is_paused = False
        self.program_thread = None
        self.listener_thread = None
        self.queue = queue.Queue()
        self.timer = None  # 添加定时器引用
        self.init_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # 绑定关闭事件

    def on_closing(self):
        # 停止所有线程和清理资源
        if self.listener_thread is not None:
            self.stop_keyboard_listener()
        self.is_paused = True  # 停止程序线程
        if self.program_thread is not None:
            self.stop_program_thread()
        if self.timer is not None:
            self.timer.cancel()  # 停止定时器
        self.root.destroy()
        os._exit(0)  # 确保程序完全退出

    def init_ui(self):
        bg_color = "white"
        frame_color = "lightgrey"
        self.root.title("Keyboard Automation")
        self.text_box = tk.Text(
            self.root,
            height=10,
            width=40,
            bg=bg_color,
            fg="black",
            font=("Helvetica", 10),
        )
        self.text_box.pack(pady=10)

        entry_frame = tk.Frame(self.root, bg=frame_color, bd=0)
        entry_frame.pack(pady=10, padx=10, fill="x")

        n_label = tk.Label(entry_frame, text="操作次数 (n):", bg=bg_color)
        n_label.grid(row=0, column=0, padx=5)
        self.n_entry = tk.Entry(entry_frame, bd=0)
        self.n_entry.grid(row=0, column=1, padx=5)
        self.n_entry.insert(tk.END, "3")

        s_label = tk.Label(entry_frame, text="操作间隔 (s):", bg=bg_color)
        s_label.grid(row=1, column=0, padx=5)
        self.s_entry = tk.Entry(entry_frame, bd=0)
        self.s_entry.grid(row=1, column=1, padx=5)
        self.s_entry.insert(tk.END, "59")

        Control_button_frame = tk.Frame(self.root, bg="lightgrey", bd=0)
        Control_button_frame.pack(pady=5, padx=10, fill="x")

        reset_button = tk.Button(
            Control_button_frame, text="重置", width=12, command=self.reset, bg=bg_color
        )
        reset_button.grid(row=0, column=0, padx=5)

        pause_button = tk.Button(
            Control_button_frame,
            text="暂停/继续",
            width=12,
            command=self.pause,
            bg=bg_color,
        )
        pause_button.grid(row=0, column=1, padx=5)

        start_button = tk.Button(
            Control_button_frame,
            text="开始",
            width=12,
            command=self.start_program_thread,
            bg=bg_color,
        )
        start_button.grid(row=0, column=2, padx=5)

        # 键盘监听
        keyboard_button_frame = tk.Frame(self.root, bg="lightgrey", bd=0)
        keyboard_button_frame.pack(pady=5, padx=10, fill="x")
        self.listener_button = tk.Button(
            keyboard_button_frame,
            text="Start Keyboard Listener",
            width=30,
            command=self.toggle_keyboard_listener,
            bg=bg_color,
        )
        self.listener_button.grid(row=0, column=1, padx=5)

        # 3TC
        preset_button_frame = tk.Frame(self.root, bg="lightgrey", bd=0)
        preset_button_frame.pack(pady=5, padx=10, fill="x")

        for i in range(3):
            button = tk.Button(
                preset_button_frame,
                text=f"{i+1}TC",
                width=12,
                command=lambda x=i + 1: self.set_preset(x),
                bg=bg_color,
            )
            button.grid(row=0, column=i, padx=5, pady=5)

        self.root.after(100, self.process_queue)

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
        self.queue.put(
            f"===Current time: {datetime.now().strftime('%H:%M:%S')}，执行{n}次{key}===\n"
        )

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

            if now >= self.end:
                self.press_keys_f(2 * n, "h", "q")
            else:
                self.press_keys_f(n, "h", "q")

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
            self.is_paused = True  # 终止线程循环
            if self.timer is not None:
                self.timer.cancel()  # 停止定时器

    def set_preset(self, tc):
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(tk.END, str(tc * 3))
        self.s_entry.delete(0, tk.END)
        self.s_entry.insert(tk.END, "59")

    def start_keyboard_listener(self):
        self.listener_active = True
        print("Keyboard listener started.")
        self.queue.put("===Keyboard listener started===\n")
        num = 20
        keyboard.add_hotkey("f1+q", lambda: self.press_keys_f(num, "f1", "q"))
        keyboard.add_hotkey("f1+w", lambda: self.press_keys_f(num, "f1", "w"))
        keyboard.add_hotkey("f1+e", lambda: self.press_keys_f(num, "f1", "e"))

        keyboard.add_hotkey("f2+q", lambda: self.press_keys_f(num, "f2", "q"))
        keyboard.add_hotkey("f2+w", lambda: self.press_keys_f(num, "f2", "w"))
        keyboard.add_hotkey("f2+e", lambda: self.press_keys_f(num, "f2", "e"))

        keyboard.add_hotkey("f3+q", lambda: self.press_keys_f(num, "f3", "q"))
        keyboard.add_hotkey("f3+w", lambda: self.press_keys_f(num, "f3", "w"))
        keyboard.add_hotkey("f3+e", lambda: self.press_keys_f(num, "f3", "e"))

        while self.listener_active:
            time.sleep(0.1)

        keyboard.unhook_all_hotkeys()

    def stop_keyboard_listener(self):
        if self.listener_active:
            self.listener_active = False
            print("Keyboard listener stopped.")
            self.queue.put("===Keyboard listener stopped===\n")

    def toggle_keyboard_listener(self):
        if self.listener_active:
            self.stop_keyboard_listener()
            self.listener_button.config(text="Stop Keyboard Listener")
        else:
            self.listener_thread = Thread(target=self.start_keyboard_listener)
            self.listener_thread.start()
            self.listener_button.config(text="Start Keyboard Listener")


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardAutomationApp(root)
    root.mainloop()

# pyinstaller --onefile --windowed AOE4v3.py
