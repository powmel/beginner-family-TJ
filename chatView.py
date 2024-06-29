import tkinter as tk
from tkinter import scrolledtext

class ChatApp:
    def __init__(self, master):
        self.master = master
        master.title("チャットアプリ")

        # メインフレーム
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # チャット表示エリア
        self.chat_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        # メッセージ入力エリア
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=(10, 0))

        self.message_entry = tk.Entry(self.input_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.input_frame, text="送信", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.add_message("あなた", message, "right")
            self.message_entry.delete(0, tk.END)
            # ここに相手の返信ロジックを追加

    def add_message(self, sender, message, align):
        self.chat_area.configure(state='normal')
        if align == "right":
            self.chat_area.insert(tk.END, f"{message}\n", "right")
            self.chat_area.insert(tk.END, f"- {sender}\n\n", "right")
        else:
            self.chat_area.insert(tk.END, f"{sender}:\n", "left")
            self.chat_area.insert(tk.END, f"{message}\n\n", "left")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def setup_tags(self):
        self.chat_area.tag_configure("right", justify="right")
        self.chat_area.tag_configure("left", justify="left")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    app.setup_tags()
    root.geometry("400x500")
    root.mainloop()