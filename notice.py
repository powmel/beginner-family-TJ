import tkinter as tk
from tkinter import messagebox
import time
import threading

# メインウィンドウの作成
root = tk.Tk()
root.title("時間指定通知アプリ")

# 時間指定の入力を促すラベルとエントリーフィールドの作成
label = tk.Label(root, text="不安になりやすい時間帯を入力してください（HH:MM）")
label.pack(pady=10)
time_entry = tk.Entry(root)
time_entry.pack(pady=5)

# 通知を表示する関数
def show_notification():
    response = messagebox.askquestion("通知", "気分はいかがですか？", icon='question', type=messagebox.YESNO, default=messagebox.NO)
    if response == 'yes':
        messagebox.showinfo("結果", "安定を選びました")
    else:
        messagebox.showinfo("結果", "不安定を選びました")
    root.quit()

# 指定時間になったら通知を表示する関数
def check_time(target_time):
    while True:
        current_time = time.strftime('%H:%M')
        if current_time == target_time:
            show_notification()
            break
        time.sleep(1)  # 1秒ごとに時間をチェック

# 開始ボタンの作成
def start_checking_time():
    target_time = time_entry.get()
    threading.Thread(target=check_time, args=(target_time,)).start()

start_button = tk.Button(root, text="開始", command=start_checking_time)
start_button.pack(pady=10)

# メインループの開始
root.mainloop()