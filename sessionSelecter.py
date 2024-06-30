import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

class SessionSelector:
    def __init__(self, master):
        self.master = master
        self.master.title("セッションを選ぼう")
        
        self.username = tk.StringVar()
        
        self.create_widgets()

    def create_widgets(self):
        # ユーザー名入力フレーム
        username_frame = tk.Frame(self.master, pady=10)
        username_frame.pack(fill='x', padx=10)

        username_label = tk.Label(username_frame, text="ユーザー名:", font=("Arial", 12))
        username_label.pack(side='left', padx=(0, 10))

        username_entry = ttk.Entry(username_frame, textvariable=self.username, font=("Arial", 12))
        username_entry.pack(side='left', expand=True, fill='x')

        # タイトルラベル
        title_label = tk.Label(self.master, text="セッションを選ぼう", font=("Arial", 14))
        title_label.pack(pady=10)

        # セッションフレーム
        self.create_session_frame('セッション1', 'lightblue')
        self.create_session_frame('セッション2', 'skyblue')
        self.create_session_frame('セッション3', 'lightcoral')

        # スタート画面に戻るボタン
        back_button = ttk.Button(self.master, text="スタート画面に戻る", command=self.return_to_start)
        back_button.pack(pady=20, side='bottom')

    def create_session_frame(self, session_name, color):
        frame = tk.Frame(self.master, bg=color, padx=10, pady=10)
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        label = tk.Label(frame, text=session_name, bg=color, font=("Arial", 12))
        label.pack(side='left')
        
        button = ttk.Button(frame, text="参加する", command=lambda: self.join_session(session_name))
        button.pack(side='right')

    def join_session(self, session_name):
        username = self.username.get().strip()
        if not username:
            messagebox.showerror("エラー", "ユーザー名を入力してください。")
            return
        
        self.master.withdraw()  # メインウィンドウを隠す
        chat_window = tk.Toplevel(self.master)
        chat_client = ChatClient(chat_window, username, session_name)
        chat_window.protocol("WM_DELETE_WINDOW", lambda: self.on_chat_close(chat_window))

    def on_chat_close(self, chat_window):
        chat_window.destroy()
        self.master.deiconify()  # メインウィンドウを再表示

    def return_to_start(self):
        self.master.destroy()  # 現在のウィンドウを削除
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "mainscene.py"))
        subprocess.Popen(["python", script_path])  # mainscene.py を実行

if __name__ == "__main__":
    root = tk.Tk()
    app = SessionSelector(root)
    root.geometry("400x500")
    root.mainloop()
