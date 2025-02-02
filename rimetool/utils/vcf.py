import os
from pypinyin import lazy_pinyin
from datetime import datetime

def main(vcf_file):
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # 从vcf文件中提取联系人姓名
    with open(vcf_file, 'r') as infile, open(f'./vcf_mycontacts.dict.yaml.txt', 'w') as outfile:
        outfile.write(
            "# 生成工具 https://github.com/whitewatercn/rimetools\n" +
            "# 生成时间 " + current_time + "\n" +
            "---\n"
        )
        # 遍历输入文件的每一行

        for line in infile:
            # 检查行是否以'FN:'开头
            if line.startswith('FN:'):
                # 获取'FN:'后面的内容
                content = line[3:]
                words = content.rstrip('\n').rsplit(' ', 1)

                if len(words) > 1:
                    # 将倒数第一个空格后面的内容移动到最前面，并删除这个空格
                    new_line = words[1] + words[0] # + '\n'
                else:
                    # 如果行中没有空格，直接将行写入输出文件
                    new_line = words[0] # + '\n'
                # outfile.write(new_line + '\n')
                # 获取行的拼音
                pinyin = ''.join(lazy_pinyin(new_line))
                # 在行的内容后面加一个tab，然后加上它的拼音，再加一个tab，然后加上数字1
                new_line_with_pinyin = new_line + '\t' + pinyin + '\t1\n'
                outfile.write(new_line_with_pinyin)



if __name__ == "__main__":
    main()