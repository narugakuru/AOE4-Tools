import time
import keyboard
import argparse
from datetime import datetime, timedelta
import tkinter as tk
from threading import Thread


def press_keys(n):
    # 按下大写H键
    keyboard.press("H")
    keyboard.release("H")

    # 按下N次Q键
    for _ in range(n):
        keyboard.press("q")
        keyboard.release("q")

    # 按下Esc键
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
    end = start + timedelta(minutes=8)  # 8分钟后的时间
    is_paused = False
    while not is_paused:
        # 获取当前时间
        now = datetime.now()
        n = int(n_entry.get())
        s = int(s_entry.get())
        print(f"===Current time: {now.strftime('%H:%M:%S')}，执行{n}次===", flush=True)
        text_box.insert(
            tk.END, f"===Current time: {now.strftime('%H:%M:%S')}，执行{n}次===\n"
        )

        if now >= end:
            press_keys(2 * n)  # 8分钟后调用press_keys(2*n)
        else:
            press_keys(n)  # 8分钟内调用press_keys(n)

        time.sleep(s)


def start_program_thread():
    program_thread = Thread(target=start_program)
    program_thread.start()


if __name__ == "__main__":
    # 创建 Tkinter 窗口
    root = tk.Tk()
    root.title("Keyboard Automation")

    # 创建文本框用于显示输出
    text_box = tk.Text(root, height=10, width=50)
    text_box.pack(pady=10)

    # 创建n值的输入框
    n_label = tk.Label(root, text="操作次数 (n):")
    n_label.pack()
    n_entry = tk.Entry(root)
    n_entry.pack()

    # 设置n值的默认值
    n_entry.insert(tk.END, "3")

    # 创建s值的输入框
    s_label = tk.Label(root, text="操作间隔 (s):")
    s_label.pack()
    s_entry = tk.Entry(root)
    s_entry.pack()

    # 设置s值的默认值
    s_entry.insert(tk.END, "59")

    # 创建按钮
    reset_button = tk.Button(root, text="重置", command=reset)
    reset_button.pack(pady=5)

    pause_button = tk.Button(root, text="暂停/继续", command=pause)
    pause_button.pack(pady=5)

    start_button = tk.Button(root, text="开始", command=start_program_thread)
    start_button.pack(pady=5)

    # 启动 Tkinter 主循环
    root.mainloop()
