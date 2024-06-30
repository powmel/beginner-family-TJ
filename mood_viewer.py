import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import os
import subprocess
import re

class MoodViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Viewer")

        self.label = tk.Label(root, text="日付を選択して記録を表示:")
        self.label.pack(pady=10)

        self.calendar = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.pack(pady=10)

        # カレンダーに日付選択イベントをバインド
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

        # リストを表示するためのフレーム
        self.list_frame = ttk.Frame(root)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # スクロール可能なフレームを作成
        self.frame = ttk.Frame(root)
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame.pack(fill="both", expand=True)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # ボタンフレームの作成
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20, side=tk.BOTTOM)

        # メイン画面に戻るボタン
        self.back_button = tk.Button(self.button_frame, text="メイン画面に戻る", command=self.show_main_page)
        self.back_button.pack(side=tk.LEFT, padx=10)

        # 日記を書くボタン
        self.write_diary_button = tk.Button(self.button_frame, text="日記を書く", command=self.show_write_diary_page)
        self.write_diary_button.pack(side=tk.RIGHT, padx=10)

        self.load_records()

    def load_records(self):
        self.records = {}
        if os.path.exists("mood_log.txt"):
            with open("mood_log.txt", "r", encoding="utf-8") as file:
                for line in file:
                    # 正規表現を使用して行を解析
                    match = re.match(r"(\d{4}/\d{2}/\d{2} \d{2}:\d{2}) Health: (\d)/5 Mood: (\d)/5 Memo: (.+)", line.strip())
                    if match:
                        date_time_str, health, mood, memo = match.groups()
                        date_str, time_str = date_time_str.split(' ')
                        date = datetime.strptime(date_str, "%Y/%m/%d").date()
                        if date not in self.records:
                            self.records[date] = []
                        self.records[date].append((time_str, health, mood, memo))

    def on_date_selected(self, event):
        selected_date = self.calendar.selection_get()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if selected_date in self.records:
            for time_str, health, mood, memo in self.records[selected_date]:
                entry_frame = ttk.Frame(self.scrollable_frame)
                entry_frame.pack(fill="x", padx=10, pady=5)

                time_label = tk.Label(entry_frame, text=f"時刻: {time_str}")
                time_label.grid(row=0, column=0, sticky="w")

                health_label = tk.Label(entry_frame, text=f"Health: {'❤️' * int(health) + '💢' * (5 - int(health))}")
                health_label.grid(row=1, column=0, sticky="w", padx=10)

                mood_label = tk.Label(entry_frame, text=f"Mood: {'★' * int(mood) + '💧' * (5 - int(mood))}")
                mood_label.grid(row=1, column=1, sticky="w", padx=10)

                if len(memo) > 30:
                    displayed_memo = memo[:30] + "…"
                else:
                    displayed_memo = memo

                memo_label = tk.Label(entry_frame, text=f"Memo: {displayed_memo}", wraplength=400)
                memo_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

                if len(memo) > 30:
                    detail_button = tk.Button(entry_frame, text="詳細", command=lambda e=entry_frame, m=memo: self.toggle_details(e, m))
                    detail_button.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    def toggle_details(self, entry_frame, memo, detail_button=None):
        if detail_button is None:
            detail_button = [b for b in entry_frame.winfo_children() if isinstance(b, tk.Button)][0]

        if detail_button.cget("text") == "詳細":
            # 詳細をスクロール可能にする
            detail_frame = tk.Frame(entry_frame)
            detail_frame.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)
            detail_canvas = tk.Canvas(detail_frame, height=100)
            detail_scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=detail_canvas.yview)
            scrollable_detail_frame = ttk.Frame(detail_canvas)
            scrollable_detail_frame.bind(
                "<Configure>",
                lambda e: detail_canvas.configure(
                    scrollregion=detail_canvas.bbox("all")
                )
            )

            detail_canvas.create_window((0, 0), window=scrollable_detail_frame, anchor="nw")
            detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
            detail_canvas.pack(side="left", fill="x", expand=True)
            detail_scrollbar.pack(side="right", fill="y")

            detail_label = tk.Label(scrollable_detail_frame, text=memo, wraplength=400)
            detail_label.pack(fill="x", padx=5, pady=5)

            detail_button.config(text="閉じる", command=lambda: self.toggle_details(entry_frame, memo, detail_button))
        else:
            for widget in entry_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()
            detail_button.config(text="詳細", command=lambda: self.toggle_details(entry_frame, memo, detail_button))

    def show_main_page(self):
        self.root.destroy()
        subprocess.Popen(["python", "mainscene.py"])  # main.py を実行

    def show_write_diary_page(self):
        self.root.destroy()
        subprocess.Popen(["python", "mood_recorder.py"])  # mood_recorder.py を実行


if __name__ == "__main__":
    root = tk.Tk()
    app = MoodViewerApp(root)
    root.mainloop()
