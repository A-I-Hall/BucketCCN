import keyboard
import socket
import time


def clientProgram():
    print("trying to connect to server")
    host = "10.12.186.43" #"10.22.28.16"  
    port = 5050 

    client_socket = socket.socket()  
    client_socket.connect((host, port)) 

    print("game connected - press 'e' to start game")
    while True:
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
            client_socket.send('r'.encode())  #restart the game
            time.sleep(0.2)

    client_socket.close()  

if __name__ == '__main__':
    clientProgram()
