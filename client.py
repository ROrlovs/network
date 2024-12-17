import socket
import threading

HEADER = 2048
PORT = 5050
FORMAT='utf-8'
DISCONNECT_MSG = "#dc"
SERVER = "192.168.1.125"
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)


halt = False

def send(msg):
    message = userID+"~"+str(msg).replace("~","")
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def listening():
    global userID
    
    while True:
        client.recv(HEADER).decode(FORMAT)
        received_data = client.recv(HEADER).decode(FORMAT)
        if received_data.split("~")[0] == userID:
            pass
        else:
            print(received_data)

def takingInput():
    userinp = str()
    while userinp != DISCONNECT_MSG:
        userinp = input()
        send(userinp)
    endProgram()

def endProgram():
    exit()

userID = int()
client.recv(HEADER).decode(FORMAT)
userID = client.recv(HEADER).decode(FORMAT)
print("MY ID IS "+userID)

listening_thread = threading.Thread(target=listening)
listening_thread.start()

input_thread = threading.Thread(target=takingInput)
input_thread.start()





