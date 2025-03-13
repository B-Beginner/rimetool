from flask import Flask, request, render_template, send_from_directory
import os
import logging
from rimetool.main import main as rimetool_main

app = Flask(__name__)
UPLOAD_FOLDER = 'gui/uploads'
OUTPUT_FOLDER = 'gui/outputs'
# 配置日志记录
logging.basicConfig(level=logging.INFO)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.info(f"收到上传请求，方法：{request.method}")
    logging.info(f"表单数据：{request.form}")
    logging.info(f"文件：{request.files}")
    
    try:
        if 'file' not in request.files:
            logging.error("没有找到文件")
            return '错误：请选择文件', 400
        file = request.files['file']
        if file.filename == '':
            return '错误：未选择文件', 400
            
        if file:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)
            output_path = os.path.join(OUTPUT_FOLDER, file.filename)
            tool = request.form['tool']
            mode = request.form.get('mode', None)
            
            args = ['--input-path', input_path, '--output-path', output_path, '--tool', tool]
            if mode:
                args.extend(['--mode', mode])
                
            try:
                rimetool_main(args)
                return send_from_directory(OUTPUT_FOLDER, file.filename)
            except Exception as e:
                logging.error(f"处理文件时发生错误: {str(e)}")
                return f'处理文件时发生错误: {str(e)}', 500
                
    except Exception as e:
        logging.error(f"上传过程中发生错误: {str(e)}")
        return f'上传过程中发生错误: {str(e)}', 500

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
