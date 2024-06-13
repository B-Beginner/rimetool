
from datetime import datetime


def main(singleword_file):
	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	with open(singleword_file, 'r') as infile, open(f'./rimetool_output/singleword.dict.yaml', 'w+') as outfile:
		outfile.write(
			"# 生成工具 https://github.com/whitewatercn/rimetools\n" +
			"# 生成时间 " + current_time + "\n" +
			"---\n"
		)
		for line in infile:
			line_without_space = line.replace(' ','').strip()
			new_line = str(line.strip() + '\t' + line_without_space + '\t'+str(1) +'\n' )
			outfile.write(new_line)



if __name__ == "__main__":
	main()