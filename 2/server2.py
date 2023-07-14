import socket
import threading
from Client import Client

import pickle           ## 비바이트 데이터를 바이트로 직렬화

def client_accept():
    child = server_sock.accept()
    print('\n===========================================\n')
    print(f'{child[1]}에서 접속')
    print(f'현재 접속자 수: {len(client_sockets) + 1}')

    return child

def send_all_msg(msg, from_sock):                       # for 문을 통해 접속된 client 모두에게 같은 msg 전송
    for client_socket in client_sockets:                # dict keys 순회
        if not client_socket == from_sock:              # 메시지를 보낸 클라이언트에게는 다시 보내지 않음
            ##msg = pickle.dumps(msg) -> 메세지 원본을 수정하면서 계속 다른 소켓들에게 보내니 오류!!!
            client_socket[0].sendall(pickle.dumps(msg))

def send_to_msg(msg, to_sock):
    msg = pickle.dumps(msg)
    to_sock[0].sendall(msg)

def recv_msg(from_client, thread_pid):
    while True:
        message = [client_sockets[from_client].nickname, from_client[0].recv(1024).decode()]      # 메세지를 보낸 유저의 닉네임과 메시지 내용을 함께 보냄
        
        if message[1] == "q!":
            disconnect_user(from_client, thread_pid)
            break                       # 해당 클라이언트의 thread를 종료!
        elif message[1][0] == '@':    # 귓속말 기능
            # nickname을 통해 해당 소켓을 찾아야 함
            try:
                split_message = message[1].split(':')
                to_nickname = split_message[0][1:]
                to_sock = nickname_dic[to_nickname]

                message[0] = '@' + message[0]
                message[1] = split_message[1].strip()
                
                send_to_msg(message, to_sock)
                print(f'{message[0]} -> {to_nickname}: {message[1]}')
            except KeyError:        # 클라이언트가 없는 유저에게 귓속말 보낼 경우 에러 메세지 반환
                send_to_msg(["Server", "해당 닉네임은 존재하지 않습니다."], from_client)
            
        else:
            send_all_msg(message, from_client)
            print(f'client({message[0]}): {message[1]}')

# 접속한 사용자 닉네임 등록
def register_user(client):
    nickname = client[0].recv(1024).decode()
    user = Client(nickname)
    
    client_sockets[client] = user
    nickname_dic[nickname] = client     # socket 객체가 복사되는 것이 아닌 기존 socket의 참조가 저장됨 -> 실질적으로 닉네임 데이터만 추가적으로 저장!!

    print(f'유저 등록: ({client[1]} -> "{user.nickname}")')

def disconnect_user(client, thread_pid):                # 클라이언트가 "q!" 를 보내면 접속을 종료하겠다는 의미
    print(f'"{client_sockets[client].nickname}" 가 접속을 종료.')
    client[0].close()
    del client_sockets[client]
    # thread 리스트에서도 삭제 필요
    # del threads[thread_pid]
   

threads = {}
threads_pid = 0

client_sockets = {}
nickname_dic = {}       # nickname으로 소켓 찾기, 복사된 

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
    
    recv_thread = threading.Thread(target=recv_msg, args=(child, threads_pid))
    recv_thread.start()
    # threads[threads_pid] = recv_thread
    # threads_pid += 1

# child_sock.close()
# parent_sock.close()

# 고민 1
# 메세지를 보낸 클라이언트 소켓으로 해당 user의 닉네임? user 정보를 알 수 있어야 함!
# + 클라이언트가 요청한 상대방의 닉네임으로도 user 정보를 접근할 수 있어야 함!
