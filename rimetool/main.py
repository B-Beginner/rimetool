import os
from rimetool.utils import vcf
from rimetool.utils import simple_english
from rimetool.utils import simple_chinese
from rimetool.utils import tosogou
from rimetool.utils import Epub_Processor
import argparse


"""
epub示例指令

1：将EPUB转换为纯文本
python rimetool/main.py -t epub -i "E:\rimetool\examples\jinkuiyaolue.epub" -o "E:\rimetool\rimetool\epub" -m epub_to_txt

2：将文本转换为短句和长句
python rimetool/main.py -t epub -i "E:\rimetool\rimetool\epub\epub转txt.txt" -o "E:\rimetool\rimetool\epub" -m txt_to_short_long

3：将文本转换为rime格式(包含了第二步)
python rimetool/main.py -t epub -i "E:\rimetool\rimetool\epub\epub转txt.txt" -o "E:\rimetool\rimetool\epub" -m txt_to_rime

4：完整的 EPUB -> txt -> rime 转换流程（包含了第一、第三步）
python rimetool/main.py -t epub -i "E:\rimetool\examples\jinkuiyaolue.epub" -o "E:\rimetool\rimetool\epub" -m epub_to_rime


其他示例指令

| rimetool --input-path 你的文件路径 --tool vcf           | 用于将联系人文件（.vcf）导出为rime词库                       |
| rimetool --input-path 你的文件路径 --tool singleword    | 将单个词（如hello）或单个词组（如hello world）文件（.txt）导出为rime词库 |
| rimetool --input-path 你的文件路径 --tool singlechinese | 将单个中文词组（如你好）文件（.txt）导出为rime词库           |
| rimetool --input-path 你的文件路径 --tool tosougou      | 将rime词库导出为搜狗txt词库                                  |

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

	parser = argparse.ArgumentParser(description='rime输入法相关工具', add_help=add_help)
	parser.add_argument('--input-path', '-i', required=True, type=str, help='需要处理的文件自身路径')
	parser.add_argument('--output-path', '-o', default='./rimetool_output', type=str, help='输出文件夹的路径')
	parser.add_argument('--tool', '-t', required=True, choices=['vcf','singleword','singlechinese','tosougou','epub','hello'], type=str, help='选择工具')
	parser.add_argument('--mode', '-m', required=False, 
						   choices=list(mode_choices.keys()),
						   help='选择EPUB处理模式：\n'
								'1/epub_to_txt: 将EPUB转换为纯文本\n'
								'2/txt_to_short_long: 将文本转换为短句和长句\n'
								'3/txt_to_rime: 将文本转换为rime格式\n'
								'4/epub_to_rime: 完整的EPUB到rime转换流程')

	return parser

def main():
	parser = get_args_parser()
	args = parser.parse_args()
	
	# if not os.path.exists('./rimetool_cache'):
		# os.makedirs('./rimetool_cache')
	if not os.path.exists(args.output_path):
		os.makedirs(args.output_path)
	os.makedirs(args.output_path, exist_ok=True)
	if args.tool == 'vcf':
		vcf.main(args.input_path, args.output_path)
	elif args.tool == 'singleword':
		simple_english.main(args.input_path, args.output_path)
	elif args.tool == 'singlechinese':
		simple_chinese.main(args.input_path, args.output_path)
	elif args.tool == 'tosougou':
		tosogou.main(args.input_path, args.output_path)
	elif args.tool == 'epub':
		output_dir = args.output_path
		# 设置各种输出文件的路径
		output_files = {
			'clean': os.path.join(output_dir, "epub转txt.txt"),  # 清理后的原始内容
			'short': os.path.join(output_dir, "短句拆分.txt"),  # 短句拆分结果
			'long': os.path.join(output_dir, "长句拆分.txt")  # 长句拆分结果
		}
		
		# 创建EpubProcessor实例
		processor = Epub_Processor.EpubProcessor(args.input_path, output_dir, output_files)
		
		# 根据选择的模式执行相应的处理
		mode = mode_choices[args.mode]
		if mode == 'epub_to_txt':
			processor.epub_to_txt()
		elif mode == 'txt_to_short_long':
			processor.txt_to_short_long(output_files)
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
