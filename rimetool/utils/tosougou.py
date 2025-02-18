from datetime import datetime
import re
import os

def main(input_file, output_path):
	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	output_file = os.path.join(output_path, f'tosougou_output.txt')

	with open(input_file, 'r') as infile, open(output_file, 'w+') as outfile:
		outfile.write(
			"# 生成工具 https://github.com/whitewatercn/rimetool\n" +
			"# 生成时间 " + current_time + "\n" +
			"---\n"
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



if __name__ == "__main__":
	main()