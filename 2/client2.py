import socket
import threading

import pickle

def recv_msg():
    while True:
        msg = client_sock.recv(1024)
        msg = pickle.loads(msg)
        print(f'({msg[0]}): {msg[1]}\n>>> ', end='')  # 보낸 유저의 닉네임과 메시지 내용을 함께 출력


def send_msg(msg):
    client_sock.sendall(msg.encode('utf-8'))        # send vs sendaall: sendall이 버퍼에 있는 데이터를 다 보냈음을 보장함!!

def disconnect_with_server():
    send_msg("q!")              # 서버 측으로 연결을 끊겠다고 알림
    print("Server와 접속을 종료")

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
recv_thread.daemon = True   # 데몬 스레드로 변경 -> 메인 스레드 종료 시 자동으로 종료
recv_thread.start()

try:
    while True:
        msg = input(">>> ")
        if msg == "q!":
            break
        send_msg(msg)
except:
    pass
finally:                    ## 프로그램이 종료하기 전 서버로 연결을 종료하는 메세지를 전송(crtl+c 도 반응)
    disconnect_with_server()


client_sock.close()
print("클라이언트 채팅 프로그램 정상적으로 종료")