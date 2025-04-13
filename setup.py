from setuptools import setup, find_packages

setup(
    # 以下为必需参数
    name='rimetool',  # 模块名
    version='1.8.1',  # 当前版本
    description='rime输入法相关工具',  # 简短描述
    packages=find_packages(include=['rimetool', 'rimetool.*']),  # 包含rimetool和rimetool下的所有子包
    
    # 以下均为可选参数
    long_description="rime输入法相关工具，将多种文件转换为rime词库，支持vcf、单个英语单词及词组，单个中文汉字及词组",# 长描述
    url='https://github.com/whitewatercn/rimetool', # 主页链接
    author='whitewatercn', # 作者名
    author_email='whitewatercn@outlook.com', # 作者邮箱
    classifiers=[
        'Intended Audience :: Developers', # 模块适用人群
        'Topic :: Software Development :: Build Tools', # 给模块加话题标签

    ],
    keywords=['rime','input method editor tool','python'],  # 模块的关键词，使用空格分割
    install_requires=['pypinyin',
					  'argparse',
					  'click',
					  'chardet'
					  ], # 依赖模块
    python_requires='>=3.0',  # 模块支持的Python版本
    entry_points={  # 新建终端命令并链接到模块函数
        'console_scripts': [
            'rimetool=rimetool.main:main',
        ],
        },
        project_urls={  # 项目相关的额外链接
        'Bug Reports': 'https://github.com/whitewatercn/rimetool/issues',
        'Source': 'https://github.com/whitewatercn/rimetool',
    },
)
