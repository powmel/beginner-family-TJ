import tkinter as tk
from tkinter import ttk
import socket
import threading

class ChatApp:
    def __init__(self, master):
        self.master = master
        self.master.title("チャットアプリ")
        self.username = "ユーザー"  # ユーザー名を設定できるようにしてもよいでしょう
        self.current_session = None
        self.client_socket = None

        self.create_session_selection_screen()

    def create_session_selection_screen(self):
        self.session_frame = tk.Frame(self.master)
        self.session_frame.pack(fill='both', expand=True)

        title_label = tk.Label(self.session_frame, text="セッションを選ぼう", font=("Arial", 14))
        title_label.pack(pady=10)

        sessions = [("セッション1", "lightblue"), ("セッション2", "skyblue"), ("セッション3", "lightcoral")]
        for session, color in sessions:
            self.create_session_frame(self.session_frame, session, color)

    def create_session_frame(self, parent, session_name, color):
        frame = tk.Frame(parent, bg=color, padx=10, pady=10)
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        label = tk.Label(frame, text=session_name, bg=color)
        label.pack(side='left')
        button = ttk.Button(frame, text="参加する", command=lambda: self.join_session(session_name))
        button.pack(side='right')

    def join_session(self, session_name):
        self.current_session = session_name
        self.session_frame.destroy()
        self.create_chat_room()
        self.connect_to_server()

    def create_chat_room(self):
        self.chat_frame = tk.Frame(self.master)
        self.chat_frame.pack(fill='both', expand=True)

        self.chat_area = tk.Text(self.chat_frame, state='disabled')
        self.chat_area.pack(fill='both', expand=True, padx=10, pady=10)

        self.input_frame = tk.Frame(self.chat_frame)
        self.input_frame.pack(fill='x', padx=10, pady=(0, 10))

        self.message_entry = tk.Entry(self.input_frame)
        self.message_entry.pack(side='left', fill='x', expand=True)

        send_button = ttk.Button(self.input_frame, text="送信", command=self.send_message)
        send_button.pack(side='right', padx=(10, 0))

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 5555))
        self.client_socket.send(f"{self.current_session}:{self.username}".encode('utf-8'))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            full_message = f"{self.username}: {message}"
            self.client_socket.send(full_message.encode('utf-8'))
            self.message_entry.delete(0, 'end')

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_area.configure(state='normal')
                self.chat_area.insert('end', message + '\n')
                self.chat_area.configure(state='disabled')
                self.chat_area.see('end')
            except:
                print("サーバーとの接続が切断されました")
                break

    def on_closing(self):
        if self.client_socket:
            self.client_socket.close()
        self.master.destroy()