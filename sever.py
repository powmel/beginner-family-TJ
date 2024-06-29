import socket
import pyaudio

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
    
    import threading
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
