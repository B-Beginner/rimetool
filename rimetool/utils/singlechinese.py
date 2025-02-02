import os
from pypinyin import lazy_pinyin
from datetime import datetime

def main(singlechinese_file):
	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	with open(singlechinese_file, 'r') as infile, open(f'./singlechinese_output.dict.yaml', 'w') as outfile:
		outfile.write(
			"# 生成工具 https://github.com/whitewatercn/rimetool\n" +
			"# 生成时间 " + current_time + "\n" +
			"---\n"
		)
		# 遍历输入文件的每一行

		for line in infile:
			content = line
			words = content.rstrip('\n').split('\t')
			new_line = words[0]
			pinyin = ''.join(lazy_pinyin(new_line))
			# 在行的内容后面加一个tab，然后加上它的拼音，再加一个tab，然后加上数字1
			new_line_with_pinyin = new_line + '\t' + pinyin + '\t1\n'
			outfile.write(new_line_with_pinyin)
		print(f"已生成文件 {os.path.abspath(outfile.name)}")

if __name__ == "__main__":
    main()