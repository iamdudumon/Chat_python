import socket
import threading

def client_accept(client_size):
    child_sock, child_addr = server_sock.accept()
    client_size += 1
    client_sockets.append([child_sock, child_addr])
    print(f'{child_addr}에서 접속')

    return client_size

def send_msg_all(msg, from_sock):                      # for 문을 통해 접속된 client 모두에게 같은 msg 전송
    for client_socket in client_sockets:
        if not client_socket == from_sock:              # 메시지를 보낸 클라이언트에게는 다시 보내지 않음
            client_socket[0].sendall(msg)

def recv_msg(from_sock):
    while True:
        message = from_sock[0].recv(1024)
        send_msg_all(message, from_sock)
        print(f'client({from_sock[1]}): {message.decode()}')
        

threads = []
threads_size = 0

client_sockets = []
client_size = 0

host = 'localhost'
port = 55555

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_sock.bind((host, port))
server_sock.listen(5)
print(f'채팅 서버 open\nhost: {host}\tport: {port}\n---------------------------------------')

while True:
    client_size = client_accept(client_size)        # 만약 연결된 클라이언트가 있으면 다음 코드로 넘어감
    print(f'현재 접속자 수: {client_size}')
    recv_thread = threading.Thread(target=recv_msg, args=(client_sockets[client_size - 1],))
    recv_thread.start()
    threads.append(recv_thread)

# child_sock.close()
# parent_sock.close()