# server.py
import socket
import threading

class ChatServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5555
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # {session: [client_sockets]}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"サーバーが {self.host}:{self.port} で起動しました")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"新しい接続: {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            session_info = client_socket.recv(1024).decode('utf-8')
            session, username = session_info.split(':', 1)
            if session not in self.clients:
                self.clients[session] = []
            self.clients[session].append(client_socket)
            
            self.broadcast(f"{username} がセッションに参加しました", session)

            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    self.broadcast(message, session)
                else:
                    break
        except:
            pass
        finally:
            self.remove_client(client_socket, session)

    def broadcast(self, message, session):
        for client in self.clients.get(session, []):
            try:
                client.send(message.encode('utf-8'))
            except:
                self.remove_client(client, session)

    def remove_client(self, client_socket, session):
        if session in self.clients and client_socket in self.clients[session]:
            self.clients[session].remove(client_socket)
            client_socket.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()