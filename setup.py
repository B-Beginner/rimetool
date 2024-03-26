from setuptools import setup, find_packages

setup(
    # 以下为必需参数
    name='rimetool',  # 模块名
    version='0.0.2',  # 当前版本
    description='rime输入法相关工具',  # 简短描述
    py_modules=["rimetool"], # 单文件模块写法
    
    # 以下均为可选参数
    long_description="rime输入法相关工具",# 长描述
    url='https://github.com/whitewatercn/rimetool', # 主页链接
    author='whitewatercn', # 作者名
    author_email='whitewatercn@outlook.com', # 作者邮箱
	packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers', # 模块适用人群
        'Topic :: Software Development :: Build Tools', # 给模块加话题标签

    ],
    keywords=['rime','input method editor tool','python'],  # 模块的关键词，使用空格分割
    install_requires=['pypinyin','click','tools'], # 依赖模块
    python_requires='>=3',  # 模块支持的Python版本
    entry_points={  # 新建终端命令并链接到模块函数
        'console_scripts': [
            'rimetool=rimetool.rimetool:main',
        ],
        },
        project_urls={  # 项目相关的额外链接
        'Bug Reports': 'https://github.com/whitewatercn/rimetool/issues',
        'Source': 'https://github.com/whitewatercn/rimetool',
    },
)
