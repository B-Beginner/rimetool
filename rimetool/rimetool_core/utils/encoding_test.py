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