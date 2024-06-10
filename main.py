import os
import utils.vcf as vcf

def get_args_parser(add_help=True):
	import argparse

	parser = argparse.ArgumentParser(description='rime输入法相关工具', add_help=add_help)
	parser.add_argument('--input-path', required=True, type=str, help='需要处理的文件路径')
	parser.add_argument('--output-path', default='./rimetool_output', type=str, help='输出文件路径')
	parser.add_argument(
		'--tool', 
		required=True,
		choices=[
			'vcf',
		   'test',
		   'hello'],
		type=str, 
		help='选择工具')
	
	return parser

def main(args):
	if not os.path.exists('./rimetool_cache'):
		os.makedirs('./rimetool_cache')
	if not os.path.exists('./rimetool_output'):
		os.makedirs('./rimetool_output')

	if args.tool == 'vcf':
		outtext = vcf.main(args.input_path)
		with open(os.path.join(args.output_path ,'vcf_output.dict.yaml'), 'w') as outfile:
			outfile.write(str(outtext))
		# print(output)
	elif args.tool == 'test':
		print(x-y)
	elif args.tool == 'hello':
		print(x*y)
	else:
		print('这里有问题')

if __name__ == "__main__":
	args = get_args_parser().parse_args()
	main(args)
