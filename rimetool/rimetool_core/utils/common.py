import chardet


def detect_file_encoding(input_file):
    encoding = None
    try:
        # 确保 gbk 文件和 utf8 文件都能正确读入
        with open(input_file, 'rb') as file:
            raw_data = file.read()
            # 检测文件编码
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            print(f"检测到的编码格式: {encoding}，置信度: {confidence}")
    except FileNotFoundError:
        print("文件未找到，请检查文件路径。")
    return encoding

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