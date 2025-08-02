from flask import Flask, render_template, request
from sender import send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    file = request.files['file']
    receiver_ip = request.form['receiver_ip']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        send_file(receiver_ip, 5001, file_path)
        message = f"✅ Gửi file đến {receiver_ip} thành công!"
    except Exception as e:
        message = f"❌ Lỗi: {str(e)}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
