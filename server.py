import socket
import json
import time
import subprocess
import os


def compress_video(original_path, compress_type, ffmpeg_path):
    COMPRESS_RATE = {"High": 23, "Medium": 30, "Low": 40}
    compressed_path = "{}/compressed.mp4".format(ffmpeg_path)

    command = [
        "ffmpeg",
        "-i",
        original_path,
        "-crf",
        "{}".format(COMPRESS_RATE[compress_type]),
        compressed_path,
    ]

    subprocess.call(command)
    return compressed_path


def handle_client(tcp_sock: socket.socket):
    # data = { "service_type": service_type, "compress_type": compress_type,"data_length": filesize}
    data = tcp_sock.recv(1024)
    print(data)

    time.sleep(1)
    # dictに変換
    request = json.loads(data.decode("utf-8"))
    print(request)

    service_type = request["service_type"]
    compress_type = request["compress_type"]
    data_length = request["data_length"]

    # 動画ファイルを取得し保存
    FFMPEG_PATH = "path/to/ffmpeg"

    if not os.path.exists(FFMPEG_PATH):
        os.makedirs(FFMPEG_PATH)

    buffer_size = 4096

    with open("{}/original-data.mp4".format(FFMPEG_PATH), "ab") as f:
        while data_length > 0:
            data = tcp_sock.recv(
                buffer_size if data_length <= buffer_size else buffer_size
            )
            f.write(data)
            data_length = data_length - len(data)
            print(data_length)

    # subprocessを使ってFFMPEGのCLIを実行する
    subprocess.call(["ffprobe", "{}/original-data.mp4".format(FFMPEG_PATH)])

    file_path = compress_video(
        "{}/original-data.mp4".format(FFMPEG_PATH), compress_type, FFMPEG_PATH
    )

    print(file_path)

    with open(file_path, "rb") as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(0, 0)

        response = {"type": service_type, "data_length": file_size}

        tcp_sock.sendall(json.dumps(response).encode("utf-8"))
        time.sleep(1)

        if file_size > pow(2, 32):
            raise Exception("ファイルの容量を2GB以下にしてください.")

        data = f.read(4096)
        while data:
            tcp_sock.send(data)
            data = f.read(4096)

    tcp_sock.close()


def start_server():
    SERVER_HOST = "localhost"
    SERVER_PORT = 8000

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((SERVER_HOST, SERVER_PORT))
    tcp_sock.listen(1)

    print("サーバーが立ち上がりました。応答を待っています")

    while True:
        connection, client_info = tcp_sock.accept()
        address, port = client_info

        print("Client: {}:{}".format(address, port))

        handle_client(connection)


def main():
    start_server()


if __name__ == "__main__":
    main()
