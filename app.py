from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from unit.license_plate_recognition import select_image, select_image1
import os
import numpy as np
from PIL import Image
import base64
import io

from unit.webcam import Webcam

# from flask import Flask, render_template
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

webcam = Webcam()

@app.route('/')
def home():
    return render_template('index.html', title = 'Parking Management')

@app.route('/uploads', methods=['POST'])
def image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        
        # Gọi hàm xử lý ảnh
        result, fileImage = select_image(file)
        
        img = Image.fromarray(fileImage.astype('uint8'))

# Tạo một đối tượng StringIO để lưu trữ dữ liệu của hình ảnh dưới dạng chuỗi
        img_io = io.BytesIO()

# Lưu hình ảnh vào đối tượng StringIO với định dạng PNG
        img.save(img_io, format='PNG')

# Mã hóa dữ liệu của hình ảnh thành chuỗi Base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode()
        
        # return render_template('index.html', result = result,fileImage =img_base64 )
        return jsonify({'message': 'File successfully uploaded', 'result': result}), 200
    return redirect(url_for('home'))


def read_from_webcam():
    while True:
        # Đọc ảnh từ class Webcam
        image = next(webcam.get_frame())
        image = select_image1(image)
        yield b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n--frame\r\n'


@app.route("/image_feed")
def image_feed():
    return Response( read_from_webcam(), mimetype="multipart/x-mixed-replace; boundary=frame" )

if __name__ == '__main__':
    app.run(debug=True)
