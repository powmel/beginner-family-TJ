import tkinter as tk
from tkinter import messagebox
import time
import threading
from datetime import datetime, timedelta
import os

# 日記ログのファイルパス
LOG_FILE = "mood_log.txt"

def read_file_with_encodings(file_path, encodings):
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.readlines()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to decode file using provided encodings: {encodings}")

def read_mood_log():
    records = []
    try:
        lines = read_file_with_encodings(LOG_FILE, ["utf-8", "utf-8-sig", "cp932", "shift_jis"])
        current_record = []
        current_date = None
        for line in lines:
            if line.strip() == "":
                if current_record:
                    records.append(current_record)
                current_record = []
            elif line.startswith("20"):  # assuming date lines start with '20'
                current_date = line.strip()
                current_record = [current_date]
            else:
                current_record.append(line.strip())
        if current_record:
            records.append(current_record)
    except UnicodeDecodeError as e:
        print(e)
    return records

def check_mood(records):
    reminders = []
    for record in records:
        if len(record) > 2 and "Health: 1/5" in record[1] and "Mood: 1/5" in record[2]:
            date_str = record[0]
            date_obj = datetime.strptime(date_str, "%Y/%m/%d %H:%M")
            next_day = date_obj + timedelta(days=1)
            reminders.append(next_day.strftime("%Y/%m/%d %H:%M"))
    print("Reminders set for: ", reminders)  # デバッグ用のログ出力
    return reminders

def show_notification():
    response = messagebox.showinfo("通知", "気分はどうですか？日記を書きましょう")
    root.quit()

def check_time(reminders):
    while True:
        current_time = datetime.now().strftime('%Y/%m/%d %H:%M')
        print("Current time: ", current_time)  # デバッグ用のログ出力
        if current_time in reminders:
            show_notification()
            break
        time.sleep(60)  # 1分ごとに時間をチェック

# メインウィンドウの作成
root = tk.Tk()
root.title("時間指定通知アプリ")

# 日記ログを読み込んで通知時間をチェック
records = read_mood_log()
reminders = check_mood(records)

# 指定時間になったら通知を表示する関数をスレッドで実行
threading.Thread(target=check_time, args=(reminders,)).start()

# メインループの開始
root.mainloop()
