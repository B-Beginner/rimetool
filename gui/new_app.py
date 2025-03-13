from flask import Flask, request, render_template, send_file
import os
import logging
from rimetool.main import main as rimetool_main

app = Flask(__name__)

# 配置日志和文件夹
UPLOAD_FOLDER = 'gui/uploads'
OUTPUT_FOLDER = 'gui/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def index():
    return render_template('new_index.html')

@app.route('/process', methods=['GET', 'POST'])
def process_file():
    if request.method == 'GET':
        return '此端点只支持 POST 请求', 405
        
    try:
        # 检查文件是否存在
        if 'file' not in request.files:
            return '请选择文件', 400
        
        file = request.files['file']
        if not file.filename:
            return '未选择文件', 400

        # 保存上传的文件
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, file.filename)
        file.save(input_path)

        # 获取参数
        tool = request.form.get('tool')
        mode = request.form.get('mode')

        # 构建参数列表
        args = ['--input-path', input_path, '--output-path', output_path, '--tool', tool]
        if mode:
            args.extend(['--mode', mode])

        # 调用处理函数
        logging.info(f'开始处理文件：{file.filename}，工具：{tool}，模式：{mode}')
        rimetool_main(args)

        # 返回处理后的文件
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        logging.error(f'处理文件时发生错误：{str(e)}')
        return f'处理文件时发生错误：{str(e)}', 500

    finally:
        # 清理临时文件
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except Exception as e:
            logging.error(f'清理临时文件时发生错误：{str(e)}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 