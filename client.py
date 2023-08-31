import socket
import sys
import tkinter as tk
import os
import json
from tkinter import filedialog
import time


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


def open_insert_file(file_entry: tk.Entry):
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Bitmap", ".bmp"),
            ("PNG", ".png"),
            ("JPEG", ".jpg"),
            ("Tiff", ".tif"),
            ("MP4", ".mp4"),
        ],
        defaultextension="bmp",
    )
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        print(file_path)


def compressor(service_type, video_path, compress_type, tcp_sock: socket.socket):
    print(service_type)
    print(compress_type)
    print(video_path)

    # 圧縮後のファイルサイズとの比較をするために事前にファイルサイズを測る
    with open(video_path, mode="rb") as f:
        f.seek(0, os.SEEK_END)
        filesize = f.tell()
        f.seek(0, 0)

        # サーバーに送るデータにする
        request = {
            "service_type": service_type,
            "compress_type": compress_type,
            "data_length": filesize,
        }
        tcp_sock.send(json.dumps(request).encode("utf-8"))
        time.sleep(1)

        if filesize > pow(2, 32):
            raise Exception("ファイルの容量を2GB以下にしてください")

        data = f.read(4096)
        while data:
            tcp_sock.send(data)
            data = f.read(4096)

    # 圧縮されたデータが返ってくるので受け取る
    res_data = tcp_sock.recv(1024)
    time.sleep(1)

    response = json.loads(res_data.decode())
    print(response)

    data_length = int(response["data_length"])

    # RESULT_PATHのファイル数を出力
    RESULT_PATH = "result"
    buffer_size = 4096
    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)

    count_files = sum(
        os.path.isfile(os.path.join(RESULT_PATH, name))
        for name in os.listdir(RESULT_PATH)
    )
    time.sleep(1)
    print(response["type"])
    if response["type"] == "compressor":
        with open(f"{RESULT_PATH}/compressed({count_files}).mp4", "ab") as f:
            while data_length > 0:
                response_file_data = tcp_sock.recv(
                    data_length if data_length <= buffer_size else buffer_size
                )
                f.write(response_file_data)
                data_length = data_length - len(response_file_data)

        print(
            "圧縮が完了しました。 圧縮されたファイルは{}/compressed({}).mp4として保存されます。".format(
                RESULT_PATH, count_files
            )
        )

    # サーバとの接続を閉じる
    tcp_sock.close()


def voice_info(service_type, video_path):
    print(service_type)
    print(video_path)


def convert_video_file_format(service_type, video_path):
    print(service_type)
    print(video_path)


def convert_video_file_to_audio_file(service_type, video_path):
    print(service_type)
    print(video_path)


def change_the_resolution_of_video_file(service_type, video_path):
    print(service_type)
    print(video_path)


def convert_time_range_of_video_to_GIF(service_type, video_path):
    print(service_type)
    print(video_path)


def handle_client(service_type, file_name, compress_type=None):
    # サーバーと接続
    tcp_sock, server_address, server_port = connect_server()

    SERVICE_TYPE = {
        "compressor": compressor,
        "voice_info": voice_info,
        "convert_video_file_format": convert_video_file_format,
        "convert_video_file_to_audio_file": convert_video_file_to_audio_file,
        "change_the_resolution_of_video_file": change_the_resolution_of_video_file,
        "convert_time_range_of_video_to_GIF": convert_time_range_of_video_to_GIF,
    }
    if service_type == "compressor":
        SERVICE_TYPE[service_type](service_type, file_name, compress_type, tcp_sock)
    else:
        SERVICE_TYPE[service_type](service_type, file_name)


def main():
    # tkinterを使ってGUIを構築する
    root = tk.Tk()

    # windowのタイトルを変更
    root.title("video-compressor-service")

    # windowのサイズの変更
    root.geometry("600x600")

    # file用のEntry
    file_entry = tk.Entry(root)
    file_entry.pack()

    # file用のButton
    file_button = tk.Button(
        root, text="ファイルを選択", command=lambda: open_insert_file(file_entry)
    )
    file_button.pack()

    ck = tk.StringVar()
    high = tk.Radiobutton(root, text="High", value="High", variable=ck)
    medium = tk.Radiobutton(root, text="Medium", value="Medium", variable=ck)
    low = tk.Radiobutton(root, text="Low", value="Low", variable=ck)

    high.pack()
    medium.pack()
    low.pack()

    compressor = tk.Button(
        root,
        text="圧縮する",
        command=lambda: handle_client("compressor", file_entry.get(), ck.get()),
    )

    voice_info = tk.Button(
        root,
        text="音声情報のみを取得する",
        command=lambda: handle_client("voice_info", file_entry.get()),
    )
    convert_video_file_format = tk.Button(
        root,
        text="動画ファイルの形式を変換する",
        command=lambda: handle_client("convert_video_file_format", file_entry.get()),
    )
    convert_video_file_to_audio_file = tk.Button(
        root,
        text="動画ファイルを音声ファイルに変換する",
        command=lambda: handle_client(
            "convert_video_file_to_audio_file", file_entry.get()
        ),
    )
    change_the_resolution_of_video_file = tk.Button(
        root,
        text="動画ファイルの解像度を変更する",
        command=lambda: handle_client(
            "change_the_resolution_of_video_file", file_entry.get()
        ),
    )
    convert_time_range_of_video_to_GIF = tk.Button(
        root,
        text="動画の時間範囲を GIF に変換する",
        command=lambda: handle_client(
            "convert_time_range_of_video_to_GIF", file_entry.get()
        ),
    )

    compressor.pack()
    voice_info.pack()

    convert_video_file_format.pack()
    convert_video_file_to_audio_file.pack()

    change_the_resolution_of_video_file.pack()
    convert_time_range_of_video_to_GIF.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
