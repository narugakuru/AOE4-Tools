import time
import keyboard
import argparse
from datetime import datetime, timedelta


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


def go(n, s):
    print("===循环开始===")
    start = datetime.now()
    end = start + timedelta(minutes=8)  # 10分钟后的时间
    while True:
        # 获取当前时间
        now = datetime.now()
        print(f"===Current time: {now.strftime('%H:%M:%S')}，执行{n}次===")

        if now >= end:
            press_keys(2 * n)  # 10分钟后调用press_keys(2*n)
        else:
            press_keys(n)  # 10分钟内调用press_keys(n)

        time.sleep(s)


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Keyboard automation script")
    parser.add_argument("-n", type=int, default=3, help="操作次数")
    parser.add_argument("-s", type=int, default=59, help="操作间隔")
    args = parser.parse_args()
    n = args.n
    s = args.s
