import socket


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server
MESSAGE = b'Hello, world!'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))  # connect to server
    client_socket.sendall(MESSAGE)  # send message to server
    print(f'TCP client sent {MESSAGE} to TCP server (serial port)')

    chunks = []
    bytes_received = 0
    while bytes_received < len(MESSAGE):
        chunk = client_socket.recv(2048)
        if chunk == b'':
            raise RuntimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_received = bytes_received + len(chunk)
    data = (b''.join(chunks).decode('utf-8'))
    print(f'TCP client {client_socket.getsockname()} received: {data} from TCP server (serial port)')






