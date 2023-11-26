import socket
import threading


def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)


nickname = input("Введіть свій нікнейм: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))
client.send(nickname.encode('utf-8'))

message_receiver = threading.Thread(target=receive_messages, args=(client,))
message_receiver.start()

while True:
    message = input()
    client.send(message.encode('utf-8'))
    if message == "/exit":
        break

client.close()
