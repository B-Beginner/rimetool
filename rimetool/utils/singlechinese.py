import os
from pypinyin import lazy_pinyin
from datetime import datetime

roman_to_chinese = {
    'Ⅰ': '一', 'Ⅱ': '二', 'Ⅲ': '三', 'Ⅳ': '四', 'Ⅴ': '五',
    'Ⅵ': '六', 'Ⅶ': '七', 'Ⅷ': '八', 'Ⅸ': '九', 'Ⅹ': '十', 
	'Ⅺ': '十一', 'Ⅻ': '十二', 'ⅩⅢ': '十三', 'ⅩⅣ': '十四', 'ⅩⅤ': '十五',
	'ⅩⅥ': '十六', 'ⅩⅦ': '十七', 'ⅩⅧ': '十八', 'ⅩⅨ': '十九', 'ⅩⅩ': '二十',
    'α': '阿尔法', 'β': '贝塔', 'γ': '伽玛', 'δ': '德尔塔', 'ε': '艾普西龙',
	'ζ': '泽塔', 'η': '伊塔', 'θ': '西塔', 'ι': '艾欧塔', 'κ': '喀帕',
    'λ': '拉姆达', 'μ': '缪', 'ν': '纽', 'ξ': '克西', 'ο': '欧米克戎',
    'π': '派', 'ρ': '柔', 'σ': '西格玛', 'τ': '陶', 'υ': '宇普西龙',
    'φ': '菲', 'χ': '卡伊', 'ψ': '普赛', 'ω': '欧米伽'

}

def replace_roman_with_chinese(text):
    for roman, chinese in roman_to_chinese.items():
        text = text.replace(roman, chinese)
    return text

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
			pinyin_line = replace_roman_with_chinese(new_line) # 将罗马数字转换为中文数字
			pinyin_line = pinyin_line.replace('-', '')  # 删除所有的 '-'
			pinyin = ''.join(lazy_pinyin(pinyin_line))
			# 在行的内容后面加一个tab，然后加上它的拼音，再加一个tab，然后加上数字1
			new_line_with_pinyin = new_line + '\t' + pinyin + '\t1\n'
			outfile.write(new_line_with_pinyin)
		print(f"已生成文件 {os.path.abspath(outfile.name)}")

if __name__ == "__main__":
    main()