import argparse
import vcf_to_dict

def main():
	# parser = argparse.ArgumentParser(description='rimetool是一个处理rime词典的工具包，详见
	parser = argparse.ArgumentParser(description='rimetool是一个处理rime词典的工具包，详见https://github.com/whitewatercn/rimetool/')
	parser.add_argument('-vcf', type=str, help='.vcf的文件路径')
	# parser.add_argument('-output', type=str, help='输出文件路径，如未指出，默认在当前目录下创建一个rimedic文件夹')
	args = parser.parse_args()
	vcf_to_dict.main(args.vcf)


if __name__ == '__main__':
	main()