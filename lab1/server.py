import socket
import threading

clients = {}


def handle_client(client_socket, username):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if message == "/exit":
            break

        broadcast(f"{username}: {message}")

    client_socket.close()
    del clients[username]
    broadcast(f"{username} вийшов з чату")


def broadcast(message):
    for client in clients.values():
        client.send(message.encode('utf-8'))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))
server.listen()

print("Сервер готовий до прийому з'єднань")

while True:
    client_socket, client_address = server.accept()
    username = client_socket.recv(1024).decode('utf-8')
    clients[username] = client_socket

    broadcast(f"{username} приєднався до чату")

    client_handler = threading.Thread(
        target=handle_client, args=(client_socket, username))
    client_handler.start()
