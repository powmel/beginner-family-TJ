import tkinter as tk
from tkinter import messagebox, font
import socket
import threading

class ChatClient:
    
    colours = {
        "backGround": "#FFF4E0",
        "chatAreaBackground": "#F0F0F0",
        "myMessageBackground": "#DCF8C6",
        "otherMessageBackground": "#FFC679"
    }
    
    def __init__(self, master, username, session_name):
        self.master = master
        self.username = username
        self.session_name = session_name
        self.master.title(f"チャットクライアント - {session_name}")
        self.master.configure(bg=self.colours["chatAreaBackground"])

        self.setup_gui()
        self.setup_network()

    def setup_gui(self):
        # フォントの設定
        self.chat_font = font.Font(family="Helvetica", size=10)
        self.input_font = font.Font(family="Helvetica", size=11)

        # チャットエリアの設定
        self.chat_frame = tk.Frame(self.master, bg=self.colours["backGround"])
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.chat_area = tk.Canvas(self.chat_frame, bg=self.colours["backGround"], highlightthickness=0)
        self.chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_area.configure(yscrollcommand=self.scrollbar.set)
        self.chat_area.bind('<Configure>', lambda e: self.chat_area.configure(scrollregion=self.chat_area.bbox("all")))

        self.inner_frame = tk.Frame(self.chat_area, bg=self.colours["backGround"])
        self.chat_area.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # 入力エリアの設定
        self.input_frame = tk.Frame(self.master, bg=self.colours["chatAreaBackground"])
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.message_entry = tk.Entry(self.input_frame, font=self.input_font, bg='#FFFFFF')
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.input_frame, text="送信", command=self.send_message, 
                                     bg='#4CAF50', fg='black', font=self.input_font)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

    def setup_network(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', 5555))
            self.client_socket.send(f"{self.session_name}:{self.username}".encode('utf-8'))

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
        except ConnectionRefusedError:
            messagebox.showerror("接続エラー", "サーバーに接続できません。サーバーが起動しているか確認してください。")
            self.master.destroy()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            try:
                full_message = f"{self.username}: {message}"
                self.client_socket.send(full_message.encode('utf-8'))
                self.message_entry.delete(0, tk.END)
                self.display_message(full_message, True)  # ローカルに表示
            except:
                messagebox.showerror("送信エラー", "メッセージを送信できません。サーバーとの接続が切断された可能性があります。")
                self.master.destroy()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message.startswith(f"{self.username}:"):  # 自分のメッセージでない場合のみ表示
                    self.display_message(message, False)
            except:
                print("サーバーとの接続が切断されました")
                self.master.destroy()
                break

    def display_message(self, message, is_own):
        frame = tk.Frame(self.inner_frame, bg=self.colours["backGround"])
        frame.pack(fill=tk.X, padx=10, pady=5)

        if is_own:
            bg_color = self.colours["myMessageBackground"]  # 自分のメッセージの背景色
            justify = tk.RIGHT
        else:
            bg_color = self.colours["otherMessageBackground"]  # 他人のメッセージの背景色
            justify = tk.LEFT

        label = tk.Label(frame, text=message, font=self.chat_font, bg=bg_color, 
                         wraplength=300, justify=justify, padx=10, pady=5)
        label.pack(side=tk.RIGHT if is_own else tk.LEFT)

        self.chat_area.update_idletasks()
        self.chat_area.yview_moveto(1)

    def on_closing(self):
        if self.client_socket:
            self.client_socket.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root, "TestUser", "TestSession")
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.geometry("400x600")
    root.mainloop()
