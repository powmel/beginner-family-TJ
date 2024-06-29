import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

class ChatClient:
    def __init__(self, master, username, session_name):
        self.master = master
        self.username = username
        self.session_name = session_name
        self.master.title(f"チャットクライアント - {session_name}")

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
            except:
                messagebox.showerror("送信エラー", "メッセージを送信できません。サーバーとの接続が切断された可能性があります。")
                self.master.destroy()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_area.configure(state='normal')
                self.chat_area.insert(tk.END, message + '\n')
                self.chat_area.configure(state='disabled')
                self.chat_area.see(tk.END)
            except:
                print("サーバーとの接続が切断されました")
                self.master.destroy()
                break

    def on_closing(self):
        if self.client_socket:
            self.client_socket.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root, "TestUser", "TestSession")
    root.protocol("WM_DELETE_WINDOW", client.on_closing)
    root.geometry("400x500")
    root.mainloop()