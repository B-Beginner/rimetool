from flask import Flask, request, render_template, make_response
import os
import logging
import traceback
from rimetool.main import main_with_args as rimetool_main
from flask_cors import CORS  # 导入 CORS
"""
使用方法：运行本文件，然后打开new_index.html，右键点击 Open in Browser 预览选项
"""
app = Flask(__name__)
# 启用 CORS
# CORS(app, origins="http://127.0.0.1:5500")  # 允许来自 http://127.0.0.1:5500 的请求
CORS(app, origins="*") 

# 配置详细的日志
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别以获取更多信息
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')

try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    logger.info(f"创建上传目录: {UPLOAD_FOLDER}")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    logger.info(f"创建输出目录: {OUTPUT_FOLDER}")
except Exception as e:
    logger.error(f"创建目录失败: {str(e)}\n{traceback.format_exc()}")

@app.route('/')
def index():
    logger.info("访问首页")
    try:
        return render_template('new_index.html')
    except Exception as e:
        logger.error(f"渲染模板失败: {str(e)}\n{traceback.format_exc()}")
        return "服务器错误", 500

@app.route('/process', methods=['POST'])
def process_file():
    logger.info("收到处理文件请求")
    input_path = None
    output_path = None

    try:
        # 检查请求内容
        logger.debug(f"请求方法: {request.method}")
        logger.debug(f"表单数据: {request.form}")
        logger.debug(f"文件数据: {request.files}")

        # 获取参数
        tool = request.form.get('tool')
        mode = request.form.get('mode')

        # 处理文件夹中的 EPUB 文件时设置默认工具
        if not tool:
        # if 'files[]' in request.files and not tool:
            tool = 'epub'

        logger.info(f"处理参数 - 工具: {tool}, 模式: {mode}")

        input_path = None
        output_path = None
        output_files = None
        if 'file' in request.files: # 非epub的单个文件
            file = request.files['file']
            if not file.filename:
                logger.warning("文件名为空")
                return make_response('请选择文件', 400)
            files = [file]
            
            # 上传文件的路径, 对单个文件而言是文件本身的路径
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_path = os.path.join(OUTPUT_FOLDER, tool+"_output")
        elif 'files[]' in request.files: # epub的文件夹
            files = request.files.getlist('files[]')
            
            if not files:
                logger.warning("请求中没有文件")
                return make_response('请选择文件', 400)
            
            # 上传文件的路径，对epub而言，是.epub文件夹的路径
            input_path = os.path.join(UPLOAD_FOLDER, files[0].filename.split("/")[0])
            output_path = os.path.join(OUTPUT_FOLDER, tool+"_output")
            # logger.info(f"🤔request.files: {request.files}")
            # output_folder = request.form.get('output_folder') # todo
        else:
            logger.warning("请求中没有文件")
            return make_response('请选择文件', 400)
        
        # logger.info(f"🤔上传文件的路径: {input_path}")
        # logger.info(f"🤔输出文件的路径: {output_path}")


        # 构建参数列表
        args = ['--input-path', input_path, '--output-path', output_path, '--tool', tool]
        if mode:
            args.extend(['--mode', mode])
        
        logger.info(f"执行命令参数: {args}")
        
        # 调用处理函数
        name = rimetool_main(args)
        
        # if not os.path.exists(output_path):
        #     logger.error(f"输出文件不存在: {output_path}")
        #     return "处理完成但输出文件未生成", 500


        logger.info(f"文件处理成功，返回处理结果信息")
        response = make_response("文件处理成功", 200)
        response.headers['Content-Type'] = 'text/plain'
        # sleep(10)
        return response
        # return send_file(output_path, as_attachment=True)

    except Exception as e:
        error_msg = f"处理文件时发生错误: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        response = make_response(error_msg, 500)
        response.headers['Content-Type'] = 'text/plain'
        return response

    finally:
        # 清理临时文件,why?因为想要另存一份文件？
        pass
        # try:
        #     if input_path and os.path.exists(input_path):
        #         os.remove(input_path)
        #         logger.info(f"清理输入文件: {input_path}")
        #     if output_path and os.path.exists(output_path):
        #         os.remove(output_path)
        #         logger.info(f"清理输出文件: {output_path}")
        # except Exception as e:
        #     logger.error(f"清理临时文件失败: {str(e)}\n{traceback.format_exc()}")

if __name__ == '__main__':
    logger.info("启动Flask应用")
    app.run(debug=True, host='0.0.0.0', port=5000)