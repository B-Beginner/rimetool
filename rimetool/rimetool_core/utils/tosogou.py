from datetime import datetime
import re
import os
from .common import detect_file_encoding

def main(input_file, output_path):
	encoding = detect_file_encoding(input_file)
	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	output_file = os.path.join(output_path, f'tosogou_output_{current_time}.txt')

	outfile=""
	with open(input_file, 'r', encoding=encoding) as infile, open(output_file, 'w+', encoding=encoding) as outfile:
		outfile.write(
			"# 生成工具 https://github.com/whitewatercn/rimetool\n" +
			"# 生成时间 " + current_time + "\n" 
			# 搜狗输入法导入时，识别"---"会报错
			# +
			# "---\n"
		)
		for line in infile:
			content = line.strip()
			if content and not content.startswith('#') and not content.startswith('---'):
				parts = content.split('\t')
				if len(parts) == 3:
					output, input, sort = parts
					new_input = "'" + input.replace(' ', "'")
					new_output = output
					new_line_output = new_output.strip().replace('-', "") + '\n'
					# 没法在这里转,有可能报bug
					outfile.write(new_line_output)

	
	print(f"已生成文件 {os.path.abspath(outfile.name)}")

	# 重新以二进制模式读取文件内容
	with open(output_file, 'rb') as f:
		content = f.read()

		# 以 GBK 编码重新写入到一个新文件中
		gbk_output_file = os.path.join(output_path, f'tosogou_output_{current_time}_gbk.txt')
		with open(gbk_output_file, 'wb') as f:
			try:
				decoded_content = content.decode(encoding)
				encoded_content = decoded_content.encode('gbk', errors='ignore')
				f.write(encoded_content)
				print(f"已将文件内容转换为 GBK 编码并保存到 {os.path.abspath(gbk_output_file)}")
			except UnicodeDecodeError:
				print("解码原文件内容时出错，请检查文件编码。")



if __name__ == "__main__":
	main()