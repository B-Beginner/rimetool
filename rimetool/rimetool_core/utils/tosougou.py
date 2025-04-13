from datetime import datetime
import re
import os
from .encoding_test import detect_file_encoding

def main(input_file, output_path, is_web=False):
	encoding = detect_file_encoding(input_file)
	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	output_file = os.path.join(output_path, f'tosougou_output_{current_time}.txt')

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
					outfile.write(new_line_output)
		print(f"已生成文件 {os.path.abspath(outfile.name)}")

	# 返回文件名，用于web下载
	filename = os.path.basename(output_file)
	if is_web:
		return output_file
	return filename



if __name__ == "__main__":
	main()