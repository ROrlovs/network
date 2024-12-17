
import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
HEADER = 2048
FORMAT='utf-8'
DISCONNECT_MSG = "#dc"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

class User:
    def __init__(self,uID,cInfo,cThread):
        self.id = uID
        self.conn = cInfo
        self.thread = cThread
        self.active = False


user_list = []

#implement later
""" def checkForExistUser(conn,addr):
    for item in user_list:
        if item.conn == conn:
            return item.id
        else:
            return False """

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    #implement later
    """userExist = checkForExistUser(conn,addr)

        if(userExist):
        final_msg = str(userExist).encode(FORMAT)
    else:
        final_msg = str(len(user_list)).encode(FORMAT) 
    """
    
    final_msg = str(len(user_list)).encode(FORMAT)
    msg_length = len(final_msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(final_msg)

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg.split("~")[1] == DISCONNECT_MSG:
                print(addr," has disconnected gracefully")
                user_list[ int( msg.split('~')[0] ) - 1 ].active = False
                sendToAllConns(f"{msg.split('~')[0]}~User {msg.split('~')[0]} has disconnected")
                connected=False
                break
            
            print("[RECEIVED]",msg)
            sendToAllConns(msg)

    
    conn.close()


def sendToAllConns(msg):
    for user in user_list:

        if not user.active: continue

        final_msg = f"{msg.split('~')[0]}~ said: {msg.split('~')[1]}"
        msg_length = len(final_msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        user.conn.send(send_length)
        user.conn.send(final_msg.encode(FORMAT))

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()

        new_user_id = len(user_list)
        new_user = User(new_user_id,conn,thread)
        user_list.append(new_user)
        user_list[ new_user_id ].active=True #set new user to active
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()