import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import os
import warnings
from pypinyin import lazy_pinyin
from datetime import datetime
from ..utils.singlechinese import replace_roman_with_chinese

# 忽略警告
warnings.filterwarnings("ignore", category=UserWarning, message="In the future version we will turn default option ignore_ncx to True.")
warnings.filterwarnings("ignore", category=FutureWarning, message="This search incorrectly ignores the root element, and will be fixed in a future version.  If you rely on the current behaviour, change it to './/xmlns:rootfile[@media - type]'")

class EpubProcessor:
    def __init__(self, input_path, output_path):
        """初始化处理器
        Args:
            input_path: EPUB文件路径
            output_path: 输出文件路径
        """
        self.input_path = input_path
        self.output_path = output_path
        self.content = ""
        self.processed_content = []
    
    def read_epub(self):
        """从EPUB文件中读取内容"""
        book = epub.read_epub(self.input_path)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                self.content += item.get_body_content().decode('utf-8')
    
    def extract_sections(self):
        """提取所有章节内容"""
        sections = re.findall(r'<.*?id=\"CHP.*?>.*?</.*?>', self.content, re.DOTALL)
        return ''.join(sections)
    
    def process_html(self, html_content):
        """处理HTML内容，提取特定标签"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取h3标签
        h3_tags = soup.find_all('div', class_='h3', id=re.compile(r'CHP\d+'))
        for tag in h3_tags:
            self.processed_content.append(str(tag))
        
        # 提取p标签
        p_tags = soup.find_all('div', class_='pCls')
        for tag in p_tags:
            self.processed_content.append(str(tag))
    
    def clean_html(self):
        """清理HTML标签，只保留文本内容"""
        final_soup = BeautifulSoup('\n'.join(self.processed_content), 'html.parser')
        for div_tag in final_soup.find_all('div'):
            div_tag.unwrap()
        return str(final_soup)
    
    def save_output(self, content):
        """保存处理结果到文件"""
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def split_into_short_sentences(self, output_path):
        """将内容拆分成短句
        Args:
            output_path: 输出文件路径
        """
        # 读取清理后的内容
        with open(self.output_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # 拆分短句
        split_content = re.split(r'[，。！？；：、\s\n]+', file_content)
        
        # 保存结果
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for item in split_content:
                if item:  # 避免写入空字符串
                    output_file.write(item + '\n')
    
    def split_into_long_sentences(self, output_path):
        """将内容拆分成无标点的长句
        Args:
            output_path: 输出文件路径
        """
        # 读取清理后的内容
        with open(self.output_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # 保存结果
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for item in file_content.split('\n'):
                if item:  # 避免写入空字符串
                    cleaned_item = re.sub(r'[^\w]', '', item)  # 移除标点符号和空格
                    output_file.write(cleaned_item + '\n')
    
    def to_rime(self, input_file, output_name):
        """将文本文件转换为rime格式
        Args:
            input_file: 输入文件路径
            output_name: 输出文件名（不含扩展名）
        """
        output_dir = os.path.dirname(self.output_path)
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = os.path.join(output_dir, f'{output_name}.dict.yaml')
        
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            # 写入文件头
            outfile.write(
                "# 生成工具 https://github.com/whitewatercn/rimetool\n" +
                "# 生成时间 " + current_time + "\n" +
                "---\n"
            )
            
            # 处理每一行
            for line in infile:
                content = line.strip()
                if not content:  # 跳过空行
                    continue
                    
                # 将罗马数字转换为中文数字
                content = replace_roman_with_chinese(content)
                # 删除所有的 '-'
                content = content.replace('-', '')
                # 生成拼音
                pinyin = ' '.join(lazy_pinyin(content))
                # 写入rime格式
                outfile.write(f"{content}\t{pinyin}\t1\n")
        
        print(f"已生成rime格式文件: {os.path.abspath(output_file)}")
        return output_file

    def process_epub(self):
        """执行完整的处理流程"""
        self.read_epub()
        sections = self.extract_sections()
        self.process_html(sections)
        final_content = self.clean_html()
        self.save_output(final_content)
        print(f"处理完成！结果已保存到: {self.output_path}")
        
        # 生成rime格式文件
        output_dir = os.path.dirname(self.output_path)
        self.to_rime(self.output_path, "clean_rime")
        self.to_rime(os.path.join(output_dir, "短句拆分.txt"), "short_rime")
        self.to_rime(os.path.join(output_dir, "长句拆分.txt"), "long_rime")

    @staticmethod
    def replace_pinyin(input_path, output_path):
        """替换拼音，如'yu'替换为'shu'"""
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                if '俞' in line:
                    line = line.replace('yu', 'shu')
                outfile.write(line)