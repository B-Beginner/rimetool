import os
from rimetool_core.utils import vcf
from rimetool_core.utils import simple_english
from rimetool_core.utils import simple_chinese
from rimetool_core.utils import tosougou
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

def main():
    parser = get_args_parser()
    args = parser.parse_args()
    
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
    os.makedirs(args.output_path, exist_ok=True)
    if args.tool == 'vcf':
        vcf.main(args.input_path, args.output_path)
    elif args.tool in ['simple-english', 'se']:
        simple_english.main(args.input_path, args.output_path)
    elif args.tool in ['simple-chinese', 'sc']:
        simple_chinese.main(args.input_path, args.output_path)
    elif args.tool == 'tosougou':
        tosogou.main(args.input_path, args.output_path)
    elif args.tool == 'epub':
        output_dir = args.output_path
        output_files = {
            'clean': os.path.join(output_dir, "epub转txt.txt"),
            'short': os.path.join(output_dir, "短句拆分.txt"),
            'long': os.path.join(output_dir, "长句拆分.txt")
        }
        processor = Epub_Processor.EpubProcessor(args.input_path, output_dir, output_files)
        
        mode = mode_choices[args.mode]
        if mode == 'epub_to_txt':
            processor.epub_to_txt()
        elif mode == 'txt_to_short_long':
            processor.txt_to_short_long(args.input_path, output_files)
        elif mode == 'txt_to_rime':
            processor.txt_to_rime_all(output_files)
        elif mode == 'epub_to_rime':
            processor.epub_to_rime(output_files)
        else:
            raise ValueError('请选择正确的EPUB处理模式')
    else:
        raise ValueError('请选择正确的工具。')

if __name__ == "__main__":
    main()