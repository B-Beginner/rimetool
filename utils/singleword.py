import os
from datetime import datetime


def main(singleword_file):
	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

	open(f'./rimetool_cache/singleword_cache_{current_time}.txt', 'w').close()


	with open(singleword_file, 'r') as infile, open(f'./rimetool_cache/singleword_cache_{current_time}.txt', 'w') as outfile:
		for line in infile:
			line_without_space = line.replace(' ','').strip()
			new_line = str(line.strip() + '\t' + line_without_space + '\t'+str(1) +'\n' )
			outfile.write(new_line)



	# 转化为rime词典格式
	with open(f'./rimetool_cache/singleword_cache_{current_time}.txt', 'r') as infile, open(f'./rimetool_output/singleword.dict.yaml', 'w+') as outfile:
		# 遍历输入文件的每一行
		for line in infile:
			outfile.write(line)
		outfile.seek(0)
		infile.close()
		outfile.close()

if __name__ == "__main__":
	main()