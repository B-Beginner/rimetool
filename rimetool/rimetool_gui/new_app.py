from flask import Flask, request, render_template, make_response, send_from_directory, send_file, jsonify, Response
import os
import logging
import traceback
import sys
import json
import zipfile  # 确保在顶部导入
import shutil
import glob  # 用于日志文件管理
from urllib.parse import quote  # 用于URL编码文件名
from flask_cors import CORS  # 导入 CORS
from datetime import datetime, time
from io import BytesIO
from pathlib import Path

try:
    from importlib import metadata as importlib_metadata
except ImportError:  # pragma: no cover
    import importlib_metadata  # type: ignore

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    try:
        import tomli as tomllib  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover
        tomllib = None

# 导入配置文件
try:
    from .gui_config import GUIConfig
except ImportError:
    from gui_config import GUIConfig
"""
使用方法：运行本文件，然后打开new_index.html，右键点击 Open in Browser 预览选项
"""


def _load_project_version() -> str:
    """Determine the rimetool project version from package metadata or pyproject."""
    try:
        return importlib_metadata.version("rimetool")
    except importlib_metadata.PackageNotFoundError:
        if tomllib is None:
            return "unknown"

        pyproject_path = Path(__file__).resolve().parent.parent.parent / "pyproject.toml"
        if not pyproject_path.exists():
            return "unknown"

        try:
            with pyproject_path.open("rb") as fp:
                data = tomllib.load(fp)
        except Exception:
            return "unknown"

        project_data = data.get("project") if isinstance(data, dict) else None
        if isinstance(project_data, dict):
            version = project_data.get("version")
            if isinstance(version, str) and version.strip():
                return version.strip()

        return "unknown"

# 获取模板文件夹的绝对路径
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = template_dir  # 将static也指向templates目录

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
# 启用 CORS，并暴露Content-Disposition头供前端JavaScript访问
# CORS(app, origins="http://localhost:5500")  # 允许来自 http://localhost:5500 的请求
CORS(app, origins="*", expose_headers=["Content-Disposition"]) 

# 配置详细的日志
# 从环境变量获取日志目录，如果没有设置则使用默认位置
log_dir = os.environ.get('RIMETOOL_LOG_DIR')
if log_dir is None:
    # 如果没有环境变量，使用当前工作目录下的 rimetool/logs
    log_dir = os.path.join(os.getcwd(), 'rimetool', 'logs')

# 确保日志目录存在
os.makedirs(log_dir, exist_ok=True)

# 生成带时间戳的日志文件名
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(log_dir, f'rimetool_gui_{timestamp}.log')

# 清理旧日志文件，保留最新的50个
def cleanup_old_logs(log_directory, max_files=50):
    pattern = os.path.join(log_directory, 'rimetool_gui_*.log')
    log_files = glob.glob(pattern)
    
    if len(log_files) > max_files:
        # 按修改时间排序，最新的在前
        log_files.sort(key=os.path.getmtime, reverse=True)
        # 删除超出数量的旧文件
        files_to_delete = log_files[max_files:]
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"已删除旧日志文件: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"删除日志文件失败 {file_path}: {e}")

# 执行日志清理
cleanup_old_logs(log_dir, 20)

logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别以获取更多信息
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 添加系统信息记录
logger.info(f"Python版本: {sys.version}")
logger.info(f"操作系统: {os.name}, {sys.platform}")
logger.info(f"当前工作目录: {os.getcwd()}")
logger.info(f"日志目录: {log_dir}")
logger.info(f"日志文件: {log_file}")

PROJECT_VERSION = _load_project_version()
logger.info(f"检测到 rimetool 版本: {PROJECT_VERSION}")

# 设置环境变量，帮助导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    logger.info(f"已添加到sys.path: {parent_dir}")

# 确保能够正确导入 rimetool_main（路径已固定，移除冗余回退逻辑）
try:
    from rimetool.main import main_with_args as rimetool_main
    logger.info("成功导入 rimetool_main")
except ImportError as e:
    logger.error(f"导入 rimetool.main:main_with_args 失败（ImportError），请确认已正确安装并在同一环境中运行。\n{str(e)}\n{traceback.format_exc()}")
    raise
except Exception as e:
    logger.error(f"导入 rimetool.main:main_with_args 时发生非导入错误: {str(e)}\n{traceback.format_exc()}")
    raise

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

# def create_meta_inf_folder(epub_folder_name, max_retries=3):
#     """创建 META-INF 文件夹并确保其存在 - EPUB功能已注销"""
#     pass

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

        # 处理文件夹中的文件时设置默认工具
        if not tool:
            # EPUB功能已注销，拒绝处理
            logger.warning("EPUB功能已注销")
            return make_response('EPUB功能已注销，请使用其他工具', 400)

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
        
        if 'zip_file' in request.files: # ZIP文件 - EPUB功能已注销
            logger.warning("EPUB功能已注销，拒绝处理ZIP文件")
            return make_response('EPUB功能已注销，请使用其他工具处理文件', 400)
        elif 'file' in request.files: # 单个文件
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
            # 检查是否上传了jieba分词库
            jieba_dict_path = None
            if 'jieba_dict' in request.files:
                jieba_dict_file = request.files['jieba_dict']
                if jieba_dict_file and jieba_dict_file.filename:
                    jieba_dict_path = os.path.join(UPLOAD_FOLDER, jieba_dict_file.filename)
                    jieba_dict_file.save(jieba_dict_path)
                    logger.info(f"jieba分词库已保存到: {jieba_dict_path}, 大小: {os.path.getsize(jieba_dict_path)} 字节")
        elif 'files[]' in request.files: # 文件夹 - EPUB功能已注销
            logger.warning("EPUB功能已注销，拒绝处理文件夹")
            return make_response('EPUB功能已注销，请使用其他工具处理文件', 400)
        else:
            logger.warning("请求中没有文件")
            return make_response('请选择文件', 400)

        # 构建参数列表
        args = ['--input-path', input_path, '--output-path', output_path, '--tool', tool]
        if mode:
            args.extend(['--mode', mode])
        # 如果上传了jieba分词库，添加参数 (使用连字符格式)
        if 'jieba_dict_path' in locals() and jieba_dict_path:
            args.extend(['--jieba-dict', jieba_dict_path])
        
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
                    # 获取原始文件名
                    original_filename = os.path.basename(output_file)
                    
                    response = send_file(
                        output_file,
                        as_attachment=True,
                        download_name=original_filename,
                        mimetype='application/octet-stream'
                    )
                    # 设置Content-Disposition，兼容所有浏览器
                    # 参考: https://www.cnblogs.com/PengZhao-Mr/p/18489371
                    # 仅使用 UTF-8 编码的文件名以简化兼容逻辑
                    encoded_filename = quote(original_filename)
                    response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_filename}"
                    logger.info(f"设置UTF-8编码文件名: {encoded_filename}")
                    # 原先的 ASCII 优先逻辑已注释：
                    # 由于前后端均已全量采用 UTF-8，且现代浏览器均支持 RFC 5987/2231 的 filename*，
                    # 暂时去掉 ASCII fallback 逻辑，避免分支复杂度与潜在不一致。
                    # 若未来需要兼容极老旧浏览器（仅识别 filename 的 ASCII），可恢复以下逻辑：
                    # try:
                    #     original_filename.encode('ascii')
                    #     response.headers["Content-Disposition"] = f'attachment; filename="{original_filename}"'
                    #     logger.info(f"文件名使用ASCII编码: {original_filename}")
                    # except UnicodeEncodeError:
                    #     encoded_filename = quote(original_filename)
                    #     response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_filename}"
                    #     logger.info(f"设置UTF-8编码文件名: {encoded_filename}")
                    
                    response.headers["Content-Type"] = "application/octet-stream"
                    response.headers["X-Content-Type-Options"] = "nosniff"
                    # 确保前端JavaScript可以访问Content-Disposition头
                    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
                    logger.info(f"返回文件: {original_filename}")
                    logger.info(f"Content-Disposition: {response.headers.get('Content-Disposition')}")
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
                            # 直接使用原始文件名（支持 UTF-8）
                            filename = os.path.basename(file_path)
                            zf.write(file_path, filename)
                        else:
                            logger.warning(f"要打包的文件不存在: {file_path}")
                
                # 获取ZIP文件大小（在seek之前）
                zip_size = memory_file.tell()
                logger.info(f"创建的ZIP文件大小: {zip_size} 字节")
                
                # 重置指针到文件开头
                memory_file.seek(0)
                
                # 使用与输出文件一致的命名格式生成ZIP文件名
                if input_path:
                    base_name = os.path.splitext(os.path.basename(input_path))[0]
                    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    safe_filename = f"{base_name}_simple_chinese_output_{current_time}.zip"
                else:
                    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    safe_filename = f"simple_chinese_output_{current_time}.zip"
                
                logger.info(f"返回ZIP文件: {safe_filename}")
                
                # 手动构建响应
                response = make_response(memory_file.getvalue())
                response.headers['Content-Type'] = 'application/zip'
                
                # 设置Content-Disposition，使用双格式兼容所有浏览器
                # 仅使用 UTF-8 编码的文件名以简化兼容逻辑
                encoded_filename = quote(safe_filename)
                response.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{encoded_filename}"
                logger.info(f"设置UTF-8编码文件名: {encoded_filename}")
                # 原先的 ASCII 优先逻辑已注释：
                # 由于前后端均已全量采用 UTF-8，且现代浏览器均支持 RFC 5987/2231 的 filename*，
                # 暂时去掉 ASCII fallback 逻辑，避免分支复杂度与潜在不一致。
                # 若未来需要兼容极老旧浏览器（仅识别 filename 的 ASCII），可恢复以下逻辑：
                # try:
                #     safe_filename.encode('ascii')
                #     response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
                #     logger.info(f"文件名使用ASCII编码: {safe_filename}")
                # except UnicodeEncodeError:
                #     encoded_filename = quote(safe_filename)
                #     response.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{encoded_filename}"
                #     logger.info(f"设置UTF-8编码文件名: {encoded_filename}")
                
                # 确保前端JavaScript可以访问Content-Disposition头
                response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
                logger.info(f"Content-Disposition已设置: {response.headers.get('Content-Disposition')}")
                
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

@app.route('/get_beian_text', methods=['GET'])
def get_beian_text():
    """Serve the Beian text from the configuration file."""
    return jsonify({"text": GUIConfig.ICP_BEIAN_TEXT})

@app.route('/get_website_config', methods=['GET'])
def get_website_config():
    """Serve the website name and title from the configuration file."""
    configured_snippet = getattr(GUIConfig, "GOOGLE_AD_SNIPPET", "")
    if isinstance(configured_snippet, str):
        configured_snippet = configured_snippet.strip()
    else:
        configured_snippet = str(configured_snippet).strip()

    google_ad_snippet = configured_snippet

    return jsonify({
        "name": GUIConfig.WEBSITE_NAME,
        "title": GUIConfig.WEBSITE_TITLE,
        "version": PROJECT_VERSION,
        "google_ad_snippet": google_ad_snippet,
        "custom_notice": getattr(GUIConfig, "CUSTOM_NOTICE_HTML", ""),
    })


@app.route('/ads.txt', methods=['GET'])
def serve_ads_txt():
    """Serve ads.txt content configured in GUIConfig."""
    content = str(getattr(GUIConfig, "ADS_TXT_LINES", ""))

    if not content:
        return Response("", mimetype='text/plain; charset=utf-8')

    if not content.endswith("\n"):
        content += "\n"

    return Response(content, mimetype='text/plain; charset=utf-8')

if __name__ == '__main__':
    logger.info("启动Flask应用")
    
    # 从环境变量读取配置
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5023))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    
    # 启动Flask应用
    app.run(debug=debug, host=host, port=port)