# Rimetools

一些rime使用工具

| 使用                                                    | 功能简介                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| rimetool --input-path 你的文件路径 --tool vcf           | 用于将联系人文件（.vcf）导出为rime词库                       |
| rimetool --input-path 你的文件路径 --tool singleword    | 将单个词（如hello）或单个词组（如hello world）文件（.txt）导出为rime词库 |
| rimetool --input-path 你的文件路径 --tool singlechinese | 将单个中文词组（如你好）文件（.txt）导出为rime词库           |
| rimetool --input-path 你的文件路径 --tool tosougou      | 将rime词库导出为搜狗txt词库                                  |

# 安装

```
pip install rimetool
```

# 使用

⚠️请查看 `examples`中相关示例文件，确保自己的原始文件符合rimetool的需求才可以转换

以 `examples/contacts.vcf`为例，这是macOS导出的通讯录，我们希望将其中的名字转换成rime词库，从而实现某些国产输入法导入通讯录的功能

其内容如下，转换前请确认你的vcf文件格式与之相符

```
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//macOS 14.5//EN
N:apple;;;;
FN:apple
TEL;type=pref:4006668800
END:VCARD
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//macOS 14.5//EN
N:hello;world;;;
FN:world hello
item1.EMAIL;type=INTERNET;type=pref:helloworld@hello.world
item1.X-ABLabel:_$!<Other>!$_
EMAIL;type=INTERNET;type=HOME:hello@world.hello
END:VCARD
BEGIN:VCARD
VERSION:3.0
PRODID:-//Apple Inc.//macOS 14.5//EN
N:你;好;;;
FN:好 你
EMAIL;type=INTERNET;type=pref:123456@qq.com
TEL;type=IPHONE;type=CELL;type=VOICE;type=pref:10086
END:VCARD
```

在终端执行

```
> rimetool --input-path examples/contacts.vcf --tool vcf
已生成文件 /Users/ww/coding/mytools/rimetool_github/contact_output.dict.yaml
```

其内容为

```
# 生成工具 https://github.com/whitewatercn/rimetools
# 生成时间 2024-06-13_16-03-02
---
apple	apple	1
helloworld	helloworld	1
你好	nihao	1
```

这样，你就得到了这份vcf通讯录文件中的人名的词库了，快快导入你的rime中吧！

# 文件结构

```.
├── README.md
├── examples #示例文件
├── rimetool #核心代码
│   ├── __init__.py
│   ├── epub #epub相关功能核心代码
│   ├── main.py #读取用户输入的输入输出路径，选择转换工具，启用utils下的各类转换工具
│   └── utils #各类转换工具的核心代码
└── setup.py #pypi相关配置文件
```



# 感谢

[manateelazycat](https://manateelazycat.github.io/)：作为开源过来人提供了思想上的帮助
[JyiDeng](https://github.com/JyiDeng)：核心开发者
# 更多

[中州韵助手](https://github.com/yanhuacuo/rimetool)：一款rime可视化配置工具，很巧也叫rimetool

