import tkinter as tk
import socket
import pyaudio
import threading

class CallApp:
    def __init__(self, master):
        self.master = master
        self.master.title("通話アプリ")

        # モード変更ボタン
        self.mode_button = tk.Button(master, text="モード変更")
        self.mode_button.pack()

        # ソートボタン
        self.sort_button = tk.Button(master, text="ソート")
        self.sort_button.pack()

        # リスト表示エリア
        self.list_frame = tk.Frame(master)
        self.list_frame.pack()

        for i in range(5):  # ダミーのリスト項目
            item = tk.Label(self.list_frame, text=f"項目 {i+1}")
            item.pack()

        # 参加ボタン
        self.join_button = tk.Button(master, text="参加", command=self.start_call)
        self.join_button.pack()

        # 通話画面ボタン
        self.call_frame = tk.Frame(master)
        self.call_frame.pack()
        for i in range(6):
            button = tk.Button(self.call_frame, text=f"参加者 {i+1}")
            button.grid(row=i//3, column=i%3)

        # 日記などのボタン
        self.diary_button = tk.Button(master, text="日記")
        self.diary_button.pack()

    def start_call(self):
        client_thread = threading.Thread(target=self.client)
        client_thread.start()

    def client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 12345))  # サーバーアドレスを指定

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)

        while True:
            data = client_socket.recv(1024)
            stream.write(data)

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established!")
        
        def handle_client(client_socket):
            while True:
                data = stream.read(1024)
                client_socket.sendall(data)
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    # サーバーを別スレッドで起動
    server_thread = threading.Thread(target=server)
    server_thread.daemon = True
    server_thread.start()

    # GUIを起動
    root = tk.Tk()
    app = CallApp(root)
    root.mainloop()
