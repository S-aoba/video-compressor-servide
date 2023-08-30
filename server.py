import socket


def start_server():
    SERVER_HOST = "localhost"
    SERVER_PORT = 8000

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((SERVER_HOST, SERVER_PORT))
    tcp_sock.listen()

    print("サーバーが立ち上がりました。応答を待っています")

    while True:
        connection, client_info = tcp_sock.accept()
        address, port = client_info

        print("Client: {}:{}".format(address, port))


def main():
    start_server()


if __name__ == "__main__":
    main()
