import socket

host = 'localhost'
port = 55555

parent_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
parent_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

parent_sock.bind((host, port))
parent_sock.listen(5)
print(f'Server IP: {host}, Port Num: {port}로 서버 실행 중...')

child_sock, child_addr = parent_sock.accept()
print(f'{child_addr}에서 접속')

while True:
    message = child_sock.recv(1024)
    print(f'{child_addr}: {message.decode()}')
    child_sock.sendall(message)

child_sock.close()
parent_sock.close()