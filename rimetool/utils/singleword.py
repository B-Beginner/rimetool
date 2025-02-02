from datetime import datetime
import re
import os

def main(singleword_file):
	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	with open(singleword_file, 'r') as infile, open(f'./singleword_output.dict.yaml', 'w+') as outfile:
		outfile.write(
			"# 生成工具 https://github.com/whitewatercn/rimetool\n" +
			"# 生成时间 " + current_time + "\n" +
			"---\n"
		)
		for line in infile:
			# 删除原单词的标点符号、空格
			line_without_space = re.sub(r'[^\w\s]', '', line).replace(' ','').strip()
			# 原单词+ tab + 去掉符合、空格的单词 + tab + 1
			new_line = str(line.strip() + '\t' + line_without_space + '\t'+str(1) +'\n' )
			outfile.write(new_line)
		print(f"已生成文件 {os.path.abspath(outfile.name)}")



if __name__ == "__main__":
	main()