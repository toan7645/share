import socket
import os

RECEIVE_FOLDER = "received"
os.makedirs(RECEIVE_FOLDER, exist_ok=True)

def start_receiver(port=5001):
    with socket.socket() as s:
        s.bind(('', port))
        s.listen(1)
        print(f"🟢 Đang chờ file tại cổng {port}...")

        conn, addr = s.accept()
        with conn:
            print(f"🔔 Kết nối từ {addr}")
            header = conn.recv(1024).decode()
            filename, filesize = header.split("|")
            filesize = int(filesize)

            conn.send(b"READY")

            save_path = os.path.join(RECEIVE_FOLDER, filename)
            with open(save_path, "wb") as f:
                total = 0
                while total < filesize:
                    data = conn.recv(4096)
                    if not data:
                        break
                    f.write(data)
                    total += len(data)

            print(f"✅ Nhận thành công: {filename}")

if __name__ == '__main__':
    start_receiver()
