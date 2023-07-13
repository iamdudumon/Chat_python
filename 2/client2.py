import socket
import threading

import pickle

start = True

def recv_msg():
    client_sock.setblocking(False)    # blocking이 True가 될 때까지 들어오는 데이터를 다 무시?
    while start:
        try:
            msg = client_sock.recv(1024)
            msg = pickle.loads(msg)
            print(f'{msg[0]}: {msg[1]}\n>>> ', end='')  # 보낸 유저의 닉네임과 메시지 내용을 함께 출력
        except BlockingIOError:
            # If recv() would have blocked, the buffer is empty
            break
    client_sock.setblocking(True)    # blocking이 True가 될 때까지 들어오는 데이터를 다 무시?

def send_msg(msg):
    client_sock.sendall(msg.encode('utf-8'))        # send vs sendaall: sendall이 버퍼에 있는 데이터를 다 보냈음을 보장함!!

server_host = 'localhost'
server_port = 55555

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 서버와 연결
client_sock.connect((server_host, server_port))
print(f'Server: {server_host}, {server_port}와 정상적으로 연결')

# 유저 정보 등록
nickname = input(">>> 사용할 닉네임을 입력하세요: ")
send_msg(nickname)

recv_thread = threading.Thread(target=recv_msg)
recv_thread.start()

while True:
    msg = input(">>> ")
    if msg == "q!":
        print("Server와 접속을 종료")
        start = False
        recv_thread.join()
        break
    send_msg(msg)

client_sock.close()
print("클라이언트 채팅 프로그램 종료")