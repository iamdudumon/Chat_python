import socket
import threading
from client import Client

import pickle           ## 비바이트 데이터를 바이트로 직렬화

def client_accept():
    child = server_sock.accept()
    print(f'{child[1]}에서 접속')
    print(f'현재 접속자 수: {len(client_sockets) + 1}')

    return child

def send_all_msg(msg, from_sock):                       # for 문을 통해 접속된 client 모두에게 같은 msg 전송
    for client_socket in client_sockets:                # dict keys 순회
        if not client_socket[0] == from_sock[0]:        # 메시지를 보낸 클라이언트에게는 다시 보내지 않음
            msg = pickle.dumps(msg)
            client_socket[0].sendall(msg)

# def send_to_msg(msg, to_sock):
#     to_sock[0].sendall(msg.encode('utf-8'))

def recv_msg(from_sock, from_address):
    while True:
        client = (from_sock, from_address)
        message = (client_sockets[client].nickname, from_sock.recv(1024).decode())       # 메세지를 보낸 유저의 닉네임과 메시지 내용을 함께 보냄
        
        send_all_msg(message, client)
        print(f'client({client_sockets[client].nickname}): {message[1]}')

# 접속한 사용자 닉네임 등록
def register_user(client_sock):
    nickname = client_sock[0].recv(1024).decode()
    user = Client(nickname)
    client_sockets[client_sock] = user

    print(f'유저 등록: ({client_sock[1]} -> "{user.nickname}")')

def disconnect_user(client_sock):
    client_sock.close()
    del client_sockets[client_sock]
        

threads = []
threads_size = 0

client_sockets = {}

host = 'localhost'
port = 55555

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind((host, port))
server_sock.listen(5)
print(f'채팅 서버 open\nhost: {host}\tport: {port}\n---------------------------------------\n\n')

while True:
    child = client_accept()        # 만약 연결된 클라이언트가 있으면 다음 코드로 넘어감
    register_user(child)
    print('\n===========================================\n')
    
    recv_thread = threading.Thread(target=recv_msg, args=(child))
    recv_thread.start()
    threads.append(recv_thread)

# child_sock.close()
# parent_sock.close()



# 고민 1
# 메세지를 보낸 클라이언트 소켓으로 해당 user의 닉네임? user 정보를 알 수 있어야 함!
# + 클라이언트가 요청한 상대방의 닉네임으로도 user 정보를 접근할 수 있어야 함!