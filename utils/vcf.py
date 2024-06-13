import os
from pypinyin import lazy_pinyin
from datetime import datetime



def main(vcf_file):
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    if not os.path.isfile(f'./rimetool_cache/vcf_cache_contacts_extracted_{current_time}.txt'):
        open(f'./rimetool_cache/vcf_cache_contacts_extracted_{current_time}.txt', 'w').close()
    if not os.path.isfile(f'./rimetool_cache/vcf_cache_contacts_without_blank_{current_time}.txt'):
        open(f'./rimetool_cache/vcf_cache_contacts_without_blank_{current_time}.txt', 'w').close()    
    if not os.path.isfile(f'./rimetool_cache/vcf_cache_mycontacts_{current_time}.dict.yaml.txt'):
        open(f'./rimetool_cache/vcf_cache_mycontacts_{current_time}.dict.yaml', 'w').close()

    # 从vcf文件中提取联系人姓名
    with open(vcf_file, 'r') as infile, open(f'./rimetool_cache/vcf_cache_contacts_extracted_{current_time}.txt', 'w') as outfile:
        # 遍历输入文件的每一行
        for line in infile:
            # 检查行是否以'FN:'开头
            if line.startswith('FN:'):
                # 获取'FN:'后面的内容
                content = line[3:]
                # 将内容写入输出文件
                outfile.write(content)


    # 去掉联系人姓名中的空格

    with open(f'./rimetool_cache/vcf_cache_contacts_extracted_{current_time}.txt', 'r') as infile, open(f'./rimetool_cache/vcf_cache_contacts_without_blank_{current_time}.txt', 'w') as outfile:
        # 遍历输入文件的每一行
        for line in infile:
            # 删除行尾的换行符
            line = line.rstrip('\n')
            # 分割行中的单词
            words = line.rsplit(' ', 1)
            # 如果行中有空格
            if len(words) > 1:
                # 将倒数第一个空格后面的内容移动到最前面，并删除这个空格
                new_line = words[1] + words[0] + '\n'
                # 将新的行写入输出文件
                outfile.write(new_line)
            else:
                # 如果行中没有空格，直接将行写入输出文件
                outfile.write(line + '\n')

    # 转化为rime词典格式
    with open(f'./rimetool_cache/vcf_cache_contacts_without_blank_{current_time}.txt', 'r') as infile, open(f'./rimetool_cache/vcf_cache_mycontacts_{current_time}.dict.yaml', 'w+') as outfile:
        # 遍历输入文件的每一行
        for line in infile:
            # 删除行尾的换行符
            line = line.rstrip('\n')
            # 获取行的拼音
            pinyin = ''.join(lazy_pinyin(line))
            # 在行的内容后面加一个tab，然后加上它的拼音，再加一个tab，然后加上数字1
            new_line = line + '\t' + pinyin + '\t1\n'
            # 将新的行写入输出文件
            outfile.write(new_line)
        outfile.seek(0)
        outtext = outfile.read()
    return outtext

if __name__ == "__main__":
    main()