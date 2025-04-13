from datetime import datetime
import re
import os
from .common import detect_file_encoding

def main(input_file, output_path, is_web=False):
	# 确保文件编码正确读入，并在输出时转为gbk
	encoding = detect_file_encoding(input_file)

	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	output_file = os.path.join(output_path, f'simple_english_output.dict_{current_time}.yaml')

	with open(input_file, 'r', encoding=encoding) as infile, open(output_file, 'w+',encoding='utf-8') as outfile:
		outfile.write(
			"# 生成工具 https://github.com/whitewatercn/rimetool\n" +
			"# 生成时间 " + current_time + "\n" +
			"---\n"
		)
		for line in infile:
			content = line
			words = content.rstrip('\n').split('\t')
			new_line = words[0]
			new_line_without_dash = new_line.replace('-', '')

			new_line_output = new_line + '\t' + new_line_without_dash + '\t1\n'



			# # 删除原单词的标点符号、空格
			# line_without_space = re.sub(r'[^\w\s]', '', line).replace(' ','').strip()
			# # 原单词+ tab + 去掉符合、空格的单词 + tab + 1
			# new_line = str(line.strip() + '\t' + line_without_space + '\t'+str(1) +'\n' )
			outfile.write(new_line_output)
		print(f"已生成文件 {os.path.abspath(outfile.name)}")

	# 返回文件名，用于web下载
	filename = os.path.basename(output_file)
	if is_web:
		return output_file
	return filename



if __name__ == "__main__":
	main()
