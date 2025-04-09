from flask import Flask, request, render_template, make_response, send_from_directory, send_file, jsonify
import os
import logging
import traceback
import sys
import json
import zipfile  # 确保在顶部导入
import shutil
from rimetool.main import main_with_args as rimetool_main
from flask_cors import CORS  # 导入 CORS
from datetime import datetime, time
from io import BytesIO
"""
使用方法：运行本文件，然后打开new_index.html，右键点击 Open in Browser 预览选项
"""
app = Flask(__name__, static_folder='templates')
# 启用 CORS
# CORS(app, origins="http://127.0.0.1:5500")  # 允许来自 http://127.0.0.1:5500 的请求
CORS(app, origins="*") 

# 配置详细的日志
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别以获取更多信息
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(r"rimetool/rimetool_gui/rimetool_gui.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 添加系统信息记录
logger.info(f"Python版本: {sys.version}")
logger.info(f"操作系统: {os.name}, {sys.platform}")
logger.info(f"当前工作目录: {os.getcwd()}")

# 设置环境变量，帮助导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    logger.info(f"已添加到sys.path: {parent_dir}")

# 确保能够正确导入rimetool_main
try:
    from rimetool.main import main_with_args as rimetool_main
    logger.info("成功导入 rimetool_main")
except ImportError as e:
    logger.error(f"导入 rimetool_main 失败: {str(e)}\n{traceback.format_exc()}")
    try:
        # 尝试不同的导入路径
        sys.path.insert(0, os.path.dirname(current_dir))
        from main import main_with_args as rimetool_main
        logger.info("使用备用路径成功导入 rimetool_main")
    except ImportError as e2:
        logger.error(f"使用备用路径导入 rimetool_main 也失败: {str(e2)}\n{traceback.format_exc()}")
        def rimetool_main(args):
            logger.error(f"无法导入真正的 rimetool_main，使用模拟函数。参数: {args}")
            return "导入模块失败，无法处理文件"

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

def create_meta_inf_folder(epub_folder_name, max_retries=3):
    """创建 META-INF 文件夹并确保其存在"""
    meta_inf_path = os.path.join(epub_folder_name, 'META-INF')
    for attempt in range(max_retries):
        try:
            if not os.path.exists(meta_inf_path):
                os.makedirs(meta_inf_path)
                logger.info(f"成功创建 META-INF 文件夹: {meta_inf_path}")
                return True
            logger.info(f"META-INF 文件夹已存在: {meta_inf_path}")
            return True
        except Exception as e:
            logger.error(f"创建 META-INF 文件夹失败 (尝试 {attempt+1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                raise e
            import time
            time.sleep(1)  # 等待一秒后重试
    return False

@app.route('/process', methods=['POST'])
def process_file():
    logger.info("收到处理文件请求")
    input_path = None
    output_path = None
    request_data = {}

    try:
        # 记录请求详细信息
        request_data = {
            "form": {k: v for k, v in request.form.items()},
            "files": [f for f in request.files.keys()],
            "headers": {k: v for k, v in request.headers.items() if k.lower() not in ['cookie', 'authorization']}
        }
        logger.info(f"请求详情: {json.dumps(request_data, indent=2)}")
        
        # 获取参数
        tool = request.form.get('tool')
        mode = request.form.get('mode')
        is_zip_file = request.form.get('is_zip_file') == 'true'
        output_folder = request.form.get('output_folder')

        # 处理文件夹中的 EPUB 文件时设置默认工具
        if not tool:
            tool = 'epub'

        # 设置默认输出路径
        if output_folder:
            custom_output_path = os.path.join(OUTPUT_FOLDER, output_folder)
            os.makedirs(custom_output_path, exist_ok=True)
            logger.info(f"使用自定义输出路径: {custom_output_path}")
        else:
            custom_output_path = None

        logger.info(f"处理参数 - 工具: {tool}, 模式: {mode}, 是否是ZIP文件: {is_zip_file}, 自定义输出路径: {custom_output_path}")

        input_path = None
        output_path = None
        output_files = None
        
        if 'zip_file' in request.files: # ZIP文件
            zip_file = request.files['zip_file']
            if not zip_file.filename:
                logger.warning("ZIP文件名为空")
                return make_response('请选择ZIP文件', 400)
            
            try:
                # 保存ZIP文件到uploads文件夹
                zip_path = os.path.join(UPLOAD_FOLDER, zip_file.filename)
                zip_file.save(zip_path)
                logger.info(f"ZIP文件已保存到: {zip_path}, 大小: {os.path.getsize(zip_path)} 字节")
                
                # 检查ZIP文件
                if not zipfile.is_zipfile(zip_path):
                    logger.error(f"文件不是有效的ZIP文件: {zip_path}")
                    return make_response('选择的文件不是有效的ZIP文件', 400)
                
                # 解压前清理同名文件夹
                extract_path = os.path.join(UPLOAD_FOLDER, os.path.splitext(zip_file.filename)[0])
                if os.path.exists(extract_path):
                    logger.info(f"删除已存在的文件夹: {extract_path}")
                    shutil.rmtree(extract_path)
                
                # 解压ZIP文件
                os.makedirs(extract_path, exist_ok=True)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # 列出ZIP中的文件
                    file_list = zip_ref.namelist()
                    logger.info(f"ZIP文件内容: {file_list[:20]}" + ("..." if len(file_list) > 20 else ""))
                    
                    # 解压到以文件名命名的文件夹
                    zip_ref.extractall(extract_path)
                    logger.info(f"ZIP文件已解压到: {extract_path}")
                    
                    # 创建META-INF文件夹
                    create_meta_inf_folder(extract_path)
                    
                    input_path = extract_path
            except Exception as e:
                logger.error(f"处理ZIP文件失败: {str(e)}\n{traceback.format_exc()}")
                return make_response(f'处理ZIP文件失败: {str(e)}', 500)
            
            # 设置输出路径
            if custom_output_path:
                output_path = custom_output_path
            else:
                output_path = os.path.join(OUTPUT_FOLDER, (tool or "epub") + "_output")
        elif 'file' in request.files: # 非epub的单个文件
            file = request.files['file']
            if not file.filename:
                logger.warning("文件名为空")
                return make_response('请选择文件', 400)
            files = [file]
            
            # 保存文件到uploads文件夹
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)
            logger.info(f"文件已保存到: {input_path}, 大小: {os.path.getsize(input_path)} 字节")
            
            # 设置输出路径
            if custom_output_path:
                output_path = custom_output_path
            else:
                output_path = os.path.join(OUTPUT_FOLDER, (tool or "default") + "_output")
        elif 'files[]' in request.files: # epub的文件夹
            files = request.files.getlist('files[]')
            
            if not files:
                logger.warning("请求中没有文件")
                return make_response('请选择文件', 400)
            
            # 创建epub文件夹并保存所有文件
            input_path = os.path.join(UPLOAD_FOLDER, files[0].filename.split("/")[0])
            os.makedirs(input_path, exist_ok=True)
            
            for file in files:
                file_path = os.path.join(input_path, file.filename.split("/")[-1])
                file.save(file_path)
                logger.info(f"文件已保存到: {file_path}")
            
            # 设置输出路径
            if custom_output_path:
                output_path = custom_output_path
            else:
                output_path = os.path.join(OUTPUT_FOLDER, (tool or "default") + "_output")
        else:
            logger.warning("请求中没有文件")
            return make_response('请选择文件', 400)

        # 构建参数列表
        args = ['--input-path', input_path, '--output-path', output_path, '--tool', tool]
        if mode:
            args.extend(['--mode', mode])
        
        logger.info(f"执行命令参数: {args}")
        
        # 调用处理函数并获取输出文件
        try:
            output_file = rimetool_main(args)
            logger.info(f"处理完成，输出文件: {output_file}")
        except Exception as e:
            logger.error(f"调用 rimetool_main 失败: {str(e)}\n{traceback.format_exc()}")
            return make_response(f'处理文件失败: {str(e)}', 500)
        
        # 如果是单个文件，直接返回
        if isinstance(output_file, str):
            if os.path.exists(output_file):
                logger.info(f"返回单个文件: {output_file}, 大小: {os.path.getsize(output_file)} 字节")
                # 使用Flask的send_file函数而不是send_from_directory来确保正确下载
                try:
                    # 创建一个仅包含 latin-1 编码的文件名
                    safe_filename = os.path.basename(output_file)
                    # 如果文件名包含非 latin-1 编码字符，使用时间戳生成一个安全的文件名
                    # 这是由于 Anaconda\Lib\http\server.py 默认使用 latin-1 编码
                    try:
                        safe_filename.encode('latin-1')
                    except UnicodeEncodeError:
                        # 提取扩展名
                        _, ext = os.path.splitext(safe_filename)
                        # 生成基于时间戳的安全文件名
                        safe_filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
                        logger.info(f"使用安全文件名: {safe_filename}")
                    
                    response = send_file(
                        output_file,
                        as_attachment=True,
                        download_name=safe_filename,
                        mimetype='application/octet-stream'
                    )
                    # 添加额外的响应头，强制浏览器下载
                    response.headers["Content-Disposition"] = f"attachment; filename={safe_filename}"
                    response.headers["Content-Type"] = "application/octet-stream"
                    response.headers["X-Content-Type-Options"] = "nosniff"
                    return response
                except Exception as e:
                    logger.error(f"返回文件失败: {str(e)}\n{traceback.format_exc()}")
                    return make_response(f"返回文件失败: {str(e)}", 500)
            else:
                logger.error(f"输出文件不存在: {output_file}")
                return make_response("处理完成但输出文件未生成", 500)
        
        # 如果是多个文件，打包成zip
        elif isinstance(output_file, list):
            try:
                memory_file = BytesIO()
                with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for file_path in output_file:
                        if os.path.exists(file_path):
                            logger.info(f"添加文件到ZIP: {file_path}, 大小: {os.path.getsize(file_path)} 字节")
                            # 使用ASCII安全的归档名
                            filename = os.path.basename(file_path)
                            try:
                                filename.encode('latin-1')
                            except UnicodeEncodeError:
                                # 如果包含非ASCII字符，使用简单名称
                                _, ext = os.path.splitext(filename)
                                filename = f"file_{output_file.index(file_path)}{ext}"
                            zf.write(file_path, filename)
                        else:
                            logger.warning(f"要打包的文件不存在: {file_path}")
                
                memory_file.seek(0)
                zip_data = memory_file.getvalue()
                logger.info(f"创建的ZIP文件大小: {len(zip_data)} 字节")
                
                # 使用ASCII安全的文件名
                safe_filename = f"{tool or 'output'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                
                response = make_response(zip_data)
                response.headers['Content-Type'] = 'application/octet-stream'
                response.headers['Content-Disposition'] = f'attachment; filename={safe_filename}'
                response.headers["X-Content-Type-Options"] = "nosniff"
                logger.info("返回ZIP文件")
                return response
            except Exception as e:
                logger.error(f"创建ZIP文件失败: {str(e)}\n{traceback.format_exc()}")
                return make_response(f"创建ZIP文件失败: {str(e)}", 500)
            
        # 未知类型
        else:
            logger.error(f"未知的输出类型: {type(output_file)}")
            return make_response(f"处理完成但输出类型未知: {type(output_file)}", 500)

    except Exception as e:
        error_msg = f"处理文件时发生错误: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        
        # 返回更详细的错误信息
        error_response = {
            'error': str(e),
            'traceback': traceback.format_exc(),
            'request_data': request_data,
            'input_path': input_path,
            'output_path': output_path
        }
        
        response = make_response(json.dumps(error_response), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates', filename)




if __name__ == '__main__':
    logger.info("启动Flask应用")
    # 在生产环境中运行，不使用自动重启
    app.run(debug=False, host='0.0.0.0', port=5001)
    
    # 或者，如果您需要调试功能但不需要自动重启：
    # from werkzeug.serving import run_simple
    # run_simple('0.0.0.0', 5001, app, use_reloader=False, use_debugger=True)