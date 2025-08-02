import socket
import os

def send_file(ip, port, file_path):
    with socket.socket() as s:
        s.connect((ip, port))
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)

        s.send(f"{filename}|{filesize}".encode())
        ack = s.recv(1024).decode()
        if ack != "READY":
            raise Exception("Receiver không sẵn sàng")

        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                s.sendall(chunk)

        print("✅ Gửi thành công")
