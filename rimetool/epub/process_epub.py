import os
from epub_tools import EpubProcessor
import argparse

def parse_args():
    """解析命令行参数"""
    #  python process_epub.py --input "输入文件.epub" --output-dir "输出目录的路径" [--rime]
    #  python process_epub.py -i "输入文件.epub" -o "输出目录的路径" [-r] 

    parser = argparse.ArgumentParser(description='处理EPUB文件并生成不同格式的输出')
    parser.add_argument('--input', '-i', required=True,
                        help='输入的EPUB文件路径')
    parser.add_argument('--output-dir', '-o', required=True,
                        help='输出目录路径')
    parser.add_argument('--rime', '-r', action='store_true',
                        help='是否生成rime格式文件')
    return parser.parse_args()

def main():
    # 解析命令行参数
    args = parse_args()
    
    # 设置输入输出文件路径
    input_path = args.input
    output_dir = args.output_dir
    
    # 设置各种输出文件的路径
    output_files = {
        'clean': os.path.join(output_dir, "清理.txt"),  # 清理后的原始内容
        'short': os.path.join(output_dir, "短句拆分.txt"),  # 短句拆分结果
        'long': os.path.join(output_dir, "长句拆分.txt")  # 长句拆分结果
    }
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理EPUB文件
    print("正在处理EPUB文件...")
    processor = EpubProcessor(input_path, output_files['clean'])
    processor.process_epub()
    print(f"EPUB文件处理完成，结果保存在: {output_files['clean']}")
    
    # 执行短句拆分
    print("\n开始短句拆分...")
    processor.split_into_short_sentences(output_files['short'])
    print(f"短句拆分完成，结果保存在: {output_files['short']}")
    
    # 执行长句拆分
    print("\n开始长句拆分...")
    processor.split_into_long_sentences(output_files['long'])
    print(f"长句拆分完成，结果保存在: {output_files['long']}")
    
    # 如果需要生成rime格式
    if args.rime:
        print("\n开始生成rime格式文件...")
        output_dir = os.path.dirname(output_files['clean'])
        processor.to_rime(output_files['clean'], "clean_rime")
        processor.to_rime(output_files['short'], "short_rime")
        processor.to_rime(output_files['long'], "long_rime")
        print("rime格式文件生成完成！")

if __name__ == "__main__":
    main()