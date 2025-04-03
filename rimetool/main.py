from datetime import datetime
import os
import sys
from rimetool.utils import Epub_Processor, vcf
from rimetool.utils import simple_english
from rimetool.utils import simple_chinese
from rimetool.utils import tosogou
import argparse

help_text = """

参数说明:

| 参数            | 说明      | 简化形式 |
| ------------- | ------- | ---- |
| --input-path  | 输入文件路径  | -i   |
| --output-path | 输出路径    | -o   |
| --tool        | 启用工具    | -t   |
| --mode        | 工具的详细功能 | -m   |
|               |         |      |

工具说明:

| 参数                    | 说明                                               | 备注                   |
| --------------------- | ------------------------------------------------ | -------------------- |
| --tool vcf            | 用于将联系人文件（.vcf）导出为rime词库                          |                      |
| --tool simple-english | 将单个词（如hello）或单个词组（如hello world）文件（.txt）导出为rime词库 | simple-english可简化为se |
| --tool simple-chinese | 将单个中文词组（如你好）文件（.txt）导出为rime词库                    | simple-chinese可简化为sc |
| --tool tosougou       | 将rime词库导出为搜狗txt词库                                |                      |
| --tool epub           | epub相关功能，需指定--mode参数                             |                      |

epub模式说明:

| 参数       | 模式                | 说明               |
| -------- | ----------------- | ---------------- |
| --mode 1 | epub_to_txt       | 将EPUB转换为纯文本      |
| --mode 2 | txt_to_short_long | 将文本转换为短句和长句      |
| --mode 3 | txt_to_rime       | 将文本转换为rime格式     |
| --mode 4 | epub_to_rime      | 完整的EPUB到rime转换流程 |

"""

# 定义模式映射
mode_choices = {
    '1': 'epub_to_txt',
    '2': 'txt_to_short_long',
    '3': 'txt_to_rime',
    '4': 'epub_to_rime',
    'epub_to_txt': 'epub_to_txt',
    'txt_to_short_long': 'txt_to_short_long',
    'txt_to_rime': 'txt_to_rime',
    'epub_to_rime': 'epub_to_rime'
}

def get_args_parser(add_help=True):
    parser = argparse.ArgumentParser(description=help_text, add_help=add_help, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--input-path', '-i', required=True, type=str)
    parser.add_argument('--output-path', '-o', default='./rimetool_output', type=str)
    parser.add_argument('--tool', '-t', required=True, choices=['vcf','simple-english','se','simple-chinese','sc','tosougou','epub','hello'], type=str)
    parser.add_argument('--mode', '-m', required=False, choices=list(mode_choices.keys()))
    return parser

def main(output_files=None):
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    parser = get_args_parser()
    args = parser.parse_args()
    name = ""
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
    os.makedirs(args.output_path, exist_ok=True)
    if args.tool == 'vcf':
        name = vcf.main(args.input_path, args.output_path)
    elif args.tool in ['simple-english', 'se']:
        name = simple_english.main(args.input_path, args.output_path)
    elif args.tool in ['simple-chinese', 'sc']:
        name = simple_chinese.main(args.input_path, args.output_path)
    elif args.tool == 'tosougou':
        name = tosogou.main(args.input_path, args.output_path)
    elif args.tool == 'epub':
        output_dir = args.output_path
        # if not output_files:
        #     print("i'm here")
        output_files = {
            'clean': os.path.join(output_dir, "epub转txt.txt"),
            'short': os.path.join(output_dir, "短句拆分.txt"),
            'long': os.path.join(output_dir, "长句拆分.txt")
        }
        # print("🤔output_files:")
        print(output_files)
        processor = Epub_Processor.EpubProcessor(args.input_path, output_dir, output_files,current_time)
        
        # print("🤔args.input_path:"+args.input_path)
        mode = mode_choices[args.mode]
        if mode == 'epub_to_txt':
            processor.epub_to_txt()
        elif mode == 'txt_to_short_long':
            processor.txt_to_short_long(args.input_path, output_files)
        elif mode == 'txt_to_rime':
            processor.txt_to_rime_all(args.input_path,output_files)
        elif mode == 'epub_to_rime':
            processor.epub_to_rime(output_files)
        else:
            raise ValueError('请选择正确的EPUB处理模式')
    else:
        raise ValueError('请选择正确的工具。')
    return name
def main_with_args(args_list):
    """
    用于在GUI中调用
    """
    original_argv = sys.argv
    sys.argv = [''] + args_list  # 设置命令行参数
    try:
        parser = get_args_parser()
        args = parser.parse_args(args_list)
        output_files = None
        print("args.tool:"+args.tool)
        if args.tool == 'epub':
            output_dir = args.output_path
            output_files = {
                'clean': os.path.join(output_dir, "epub转txt.txt"),
                'short': os.path.join(output_dir, "短句拆分.txt"),
                'long': os.path.join(output_dir, "长句拆分.txt")
            }
            # 这里可以根据需要将 output_files 以某种方式传递给后续处理逻辑
            # 比如将其添加到 args 对象中
            # setattr(args, 'output_files', output_files)
            sys.argv = [''] + args_list 
            # + [f"--output-files={output_files}"]  # 这行可根据实际情况调整
        name = main(output_files)
    finally:
        sys.argv = original_argv  # 恢复原始的命令行参数
    return name

if __name__ == "__main__":
    main()