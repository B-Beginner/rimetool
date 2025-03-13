from flask import Flask, request, render_template, send_file
import os
import logging
import traceback
from rimetool.main import main as rimetool_main

app = Flask(__name__)

# 配置详细的日志
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别以获取更多信息
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'gui/uploads'
OUTPUT_FOLDER = 'gui/outputs'

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

        if 'file' not in request.files:
            logger.warning("请求中没有文件")
            return '请选择文件', 400
        
        file = request.files['file']
        if not file.filename:
            logger.warning("文件名为空")
            return '未选择文件', 400

        # 保存上传的文件
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, file.filename)
        
        logger.info(f"保存上传文件到: {input_path}")
        file.save(input_path)
        
        # 获取参数
        tool = request.form.get('tool')
        mode = request.form.get('mode')
        logger.info(f"处理参数 - 工具: {tool}, 模式: {mode}")

        # 构建参数列表
        args = ['--input-path', input_path, '--output-path', output_path, '--tool', tool]
        if mode:
            args.extend(['--mode', mode])
        
        logger.info(f"执行命令参数: {args}")
        
        # 调用处理函数
        rimetool_main(args)
        
        if not os.path.exists(output_path):
            logger.error(f"输出文件不存在: {output_path}")
            return "处理完成但输出文件未生成", 500

        logger.info(f"文件处理成功，准备返回: {output_path}")
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        error_msg = f"处理文件时发生错误: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return error_msg, 500

    finally:
        # 清理临时文件
        try:
            if input_path and os.path.exists(input_path):
                os.remove(input_path)
                logger.info(f"清理输入文件: {input_path}")
            if output_path and os.path.exists(output_path):
                os.remove(output_path)
                logger.info(f"清理输出文件: {output_path}")
        except Exception as e:
            logger.error(f"清理临时文件失败: {str(e)}\n{traceback.format_exc()}")

if __name__ == '__main__':
    logger.info("启动Flask应用")
    app.run(debug=True, host='0.0.0.0', port=5000) 