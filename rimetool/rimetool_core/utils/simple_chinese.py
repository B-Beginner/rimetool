import os
from pypinyin import lazy_pinyin
from datetime import datetime
from .encoding_test import detect_file_encoding
from .roman_to_chinese import roman_to_chinese



def main(input_file, output_path, is_web=False):
	# 确保文件编码正确读入，并在输出时转为gbk
	encoding = detect_file_encoding(input_file)
	
	current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	output_file = os.path.join(output_path, f'simple_chinese_output_{current_time}.dict.yaml')
	with open(input_file, 'r', encoding=encoding) as infile, open(output_file, 'w', encoding='utf-8') as outfile:
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
			pinyin_line = roman_to_chinese(new_line) # 将罗马转换为中文
			pinyin_line = pinyin_line.replace('-', '')  # 删除所有的 '-'
			pinyin = ' '.join(lazy_pinyin(pinyin_line))
			# 在行的内容后面加一个tab，然后加上它的拼音，再加一个tab，然后加上数字1
			new_line_with_pinyin = new_line + '\t' + pinyin + '\t1\n'
			outfile.write(new_line_with_pinyin)
		print(f"已生成文件 {os.path.abspath(outfile.name)}")
		
    # 返回文件名，用于web下载
	filename = os.path.basename(output_file)
	if is_web:
		return output_file
	return filename

if __name__ == "__main__":
    main()