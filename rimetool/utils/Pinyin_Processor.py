from pypinyin import lazy_pinyin
import re


def pinyin_process(input_character):
	content = input_character
	words = content.rstrip('\n').split('\t')
	new_line = words[0]
	new_line = re.sub(r'[^\w]', '', new_line)  # 移除标点符号和空格
	output_pinyin = ' '.join(lazy_pinyin(new_line))
	return output_pinyin