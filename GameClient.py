import keyboard
import socket
import time


def client_program():
    print("trying to connect to server")
    host = "10.22.28.16"  # replace with your server's IP
    port = 5050  # socket server port number

    client_socket = socket.socket()  # instantiate socket
    client_socket.connect((host, port))  # connect to the server

    print("waiting for keyboard input - press 'e' to start")
    while True:
        if keyboard.is_pressed('q'):
            break  # quit client

        if keyboard.is_pressed('e'):
            client_socket.send('e'.encode())
            time.sleep(0.2)

        if keyboard.is_pressed('a'):
            client_socket.send('a'.encode())
            time.sleep(0.1)
        if keyboard.is_pressed('d'):
            client_socket.send('d'.encode())
            time.sleep(0.1)
        if keyboard.is_pressed('w'):
            client_socket.send('w'.encode())
            time.sleep(0.1)
        if keyboard.is_pressed('s'):
            client_socket.send('s'.encode())
            time.sleep(0.1)

        if keyboard.is_pressed('r'):
            client_socket.send('r'.encode())  # send 'r' to restart the game
            time.sleep(0.2)

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
