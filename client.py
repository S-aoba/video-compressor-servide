import socket
import sys






def connect_server():
   SERVER_HOST = "localhost"
   SERVER_PORT = 8000

   tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
        tcp_sock.connect((SERVER_HOST, SERVER_PORT))
   except socket.error as err:
        print(err)
        sys.exit(1)

   print("サーバーと接続しました。")

   return tcp_sock, SERVER_HOST, SERVER_PORT



def main():
    tcp_sock, server_address, server_port = connect_server()



if __name__ == "__main__":
  main()
