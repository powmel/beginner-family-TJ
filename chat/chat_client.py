import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import json

class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("チャットクライアント")

        self.username = tk.StringVar()
        self.username.set("ユーザー名")

        self.setup_gui()
        self.setup_network()

    def setup_gui(self):
        self.chat_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.message_entry = tk.Entry(self.input_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.send_button = tk.Button(self.input_frame, text="送信", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

    def setup_network(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 5555))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            full_message = f"{self.username.get()}: {message}"
            self.client_socket.send(full_message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_area.configure(state='normal')
                self.chat_area.insert(tk.END, message + '\n')
                self.chat_area.configure(state='disabled')
                self.chat_area.see(tk.END)
            except:
                print("接続が切断されました")
                break

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.geometry("400x500")
    root.mainloop()