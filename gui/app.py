from flask import Flask, request, render_template, send_from_directory
import os
from rimetool.main import main as rimetool_main

app = Flask(__name__)
UPLOAD_FOLDER = 'gui/uploads'
OUTPUT_FOLDER = 'gui/outputs'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)
        output_path = os.path.join(OUTPUT_FOLDER, file.filename)
        tool = request.form['tool']
        mode = request.form.get('mode', None)
        args = ['--input-path', input_path, '--output-path', output_path, '--tool', tool]
        if mode:
            args.extend(['--mode', mode])
        rimetool_main(args)
        return send_from_directory(OUTPUT_FOLDER, file.filename)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)
