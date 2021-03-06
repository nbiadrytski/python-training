import socket
import serial.threaded
import sys


class SerialToNet(serial.threaded.Protocol):
    """serial->socket"""

    def __init__(self):
        self.socket = None

    def __call__(self):
        return self

    def data_received(self, data):
        if self.socket is not None:
            print(f'Serial received {data} from TCP client')
            self.socket.sendall(data)


ser = serial.serial_for_url('/dev/tty.usbserial-14200', 115200)
ser_to_net = SerialToNet()
serial_worker = serial.threaded.ReaderThread(ser, ser_to_net)
serial_worker.start()


HOST = '127.0.0.1'
PORT = 65432

# AF_INET - address family, SOCK_STREAM - socket type for TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
    # bring up the server, run the client against it, and then try killing and rerunning the server
    # OSError: [Errno 98] Address already in use
    # The answer is that once a connected TCP connection is finally closed,
    # operating system’s network stack actually keeps a record of it around for up to four minutes in a waiting state.
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind() tells your OS what are the network interfaces from which you are willing to receive connections
    # if you run server with an empty string for the hostname,
    # which tells Python bind() routine
    # that you are willing to accept connections through any of your machine’s active network interfaces
    # 0.0.0.0 to mean “accept connections on any interface”
    listen_socket.bind((HOST, PORT))
    # listen() enables a server to accept() connections. It makes it a “listening” socket.
    listen_socket.listen(1)  # 1 is number of waiting connections allowed
    # connection_socket is the socket to communicate with the client
    connection_socket, client_address = listen_socket.accept()  # blocks and waits for an incoming connection
    print(f'TCP client {client_address} connected to TCP Server (serial) {connection_socket.getsockname()}')
    try:
        ser_to_net.socket = connection_socket  # enter network <-> serial loop
        while True:
            try:
                # receiving data from client socket
                data = connection_socket.recv(2048)
                if not data:
                    break
                ser.flush()  # flush before sending data
                ser.write(data)  # serial sends received data back to tcp client
                print(f'Serial sent: {data.decode("utf-8")} to TCP client')
            except socket.error as msg:
                sys.stderr.write('ERROR: {}\n'.format(msg))
                break
    except socket.error as msg:
        sys.stderr.write('ERROR: {}\n'.format(msg))

serial_worker.stop()
    # with connection_socket:
    #     print(f'Client {client_address} connected to Server {connection_socket.getsockname()}')
    #     while True:
    #         data = connection_socket.recv(1024)  # reads whatever data the client sends
    #         if not data:
    #             break
    #         connection_socket.sendall(data)  # echoes data back to client

# after starting the server see the current state of sockets on your host
# $ netstat -an
# Active Internet connections (including servers)
# Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)
# tcp4       0      0  127.0.0.1.65432        *.*                    LISTEN

# lsof gives you the COMMAND, PID (process id), and USER (user id) of open Internet sockets
# $ lsof -i -n
# COMMAND     PID   USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME
# Python    67982 nathan    3u  IPv4 0xecf272      0t0  TCP *:65432 (LISTEN)
