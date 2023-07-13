import socket
import threading

def recv_msg():
    while True:
        msg = client_sock.recv(1024)
        print(f'Server: {msg.decode()}\n>>> ', end='')

def send_msg(msg):
    client_sock.sendall(msg.encode('utf-8'))        # send vs sendaall: sendall이 버퍼에 있는 데이터를 다 보냈음을 보장함!!

server_host = 'localhost'
server_port = 55555

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#서버와 연결
client_sock.connect((server_host, server_port))
print(f'Server: {server_host}, {server_port}와 정상적으로 연결')

recv_thread = threading.Thread(target=recv_msg)
recv_thread.start()

while True:
    msg = input(">>> ")
    send_msg(msg)

client_sock.close()
