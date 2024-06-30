import tkinter as tk
from tkinter import font
import subprocess
import os


# メインアプリケーションクラス
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # メイン画面の設定
        self.title("メイン画面")
        self.geometry("400x500")
        self.configure(bg="#E6E6FA")  # 背景色を淡い青色に設定
        
         # カスタムフォントの作成
        self.custom_font = font.Font(family="Arial", size=14, weight="bold")
        
        # タイトルラベル
        self.title_label = tk.Label(self, text="メインメニュー", font=("Arial", 20), bg="#E6E6FA", fg="#00008B")  # 背景色と文字色を設定
        self.title_label.pack(pady=20)

        # ボタンフレームの作成
        self.button_frame = tk.Frame(self, bg="#E6E6FA")  # フレームの背景色を設定
        self.button_frame.pack(expand=True)

        # ボタンの色設定
        session_button_bg_color = "#B0E0E6"  # セッションを選ぶボタンの背景色
        diary_write_button_bg_color = "#FFFACD"  # 日記を書くボタンの背景色
        diary_read_button_bg_color = "#FFCC99"  # 日記を読むボタンの背景色
        button_fg_color = "#00008B"  # ボタンの文字色

        # 「セッションを選ぶ」ボタン
        self.session_button = tk.Button(self.button_frame, text="セッションを選ぶ", command=self.show_session_page, font=self.custom_font, bg=session_button_bg_color, fg=button_fg_color, width=20, height=2)
        self.session_button.pack(pady=10)

        # 「日記を書く」ボタン
        self.write_diary_button = tk.Button(self.button_frame, text="日記を書く", command=self.write_diary_page, font=self.custom_font, bg=diary_write_button_bg_color, fg=button_fg_color, width=20, height=2)
        self.write_diary_button.pack(pady=10)

        # 「日記を読む」ボタン
        self.read_diary_button = tk.Button(self.button_frame, text="日記を読む", command=self.read_diary_page, font=self.custom_font, bg=diary_read_button_bg_color, fg=button_fg_color, width=20, height=2)
        self.read_diary_button.pack(pady=10)

    # 「セッションを選ぶ」ページを表示するメソッド
    def show_session_page(self):
        self.destroy()  # メイン画面を削除
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "sessionSelecter.py"))
        subprocess.Popen(["python", script_path])  # sessionSelecter.py を実行

    # 「日記を書く」ページを表示するメソッド
    def write_diary_page(self):
        self.destroy()  # メイン画面を削除
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "mood_recorder.py"))
        subprocess.Popen(["python", script_path])  # mood_recorder.py を実行

    # 「日記を読む」ページを表示するメソッド
    def read_diary_page(self):
        self.destroy()  # メイン画面を削除
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "mood_viewer.py"))
        subprocess.Popen(["python", script_path])  # mood_viewer.py を実行

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()