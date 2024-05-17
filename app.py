from flask import Flask, render_template, request, redirect, url_for, jsonify
# from unit.test import select_image
import os
import numpy as np
from PIL import Image
import base64
import io

# from flask import Flask, render_template
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/uploads', methods=['POST'])
# def image():
#     if 'file' not in request.files:
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         return redirect(request.url)
#     if file:
        
#         # Gọi hàm xử lý ảnh
#         result, fileImage = select_image(file)
        
#         img = Image.fromarray(fileImage.astype('uint8'))

# # Tạo một đối tượng StringIO để lưu trữ dữ liệu của hình ảnh dưới dạng chuỗi
#         img_io = io.BytesIO()

# # Lưu hình ảnh vào đối tượng StringIO với định dạng PNG
#         img.save(img_io, format='PNG')

# # Mã hóa dữ liệu của hình ảnh thành chuỗi Base64
#         img_base64 = base64.b64encode(img_io.getvalue()).decode()
        
#         # return render_template('index.html', result = result,fileImage =img_base64 )
#         return jsonify({'message': 'File successfully uploaded', 'result': result}), 200
#     return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
