# server.py
import socket
import threading
import os

HOST = '0.0.0.0'
PORT = int(os.environ.get("PORT", 12345))
clients = []

def handle_client(client_socket, addr):
    print(f"[NEW] Connected: {addr}")
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message.encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server running on port {PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    main()