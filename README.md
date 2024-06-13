# Rimetools

一些rime使用工具


| 使用         | 功能简介                 |
| ---------------- | ----------------------- |
| rimetool --inputpath 你的文件路径 --tool vcf | 用于将联系人文件（.vcf）导出为rime词库 |
|rimetool --inputpath 你的文件路径 --tool singleword|将单个词（如hello）或单个词组（如hello world）文件（.txt）导出为rime词库|



# 示例（以.vcf转换为例）

`sample_input`中的`vcf_sample.vcf`是一个小例子，里面的内容为

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
rimetool --input-path sample_input/vcf_sample.vcf --tool vcf
```

你将在`rimetool_output`文件夹下找到`vcf_mycontacts.dict.yaml`，内容为

```
# 生成工具 https://github.com/whitewatercn/rimetools
# 生成时间 2024-06-13_16-03-02
---
apple	apple	1
helloworld	helloworld	1
你好	nihao	1
```

这样，你就得到了这份vcf通讯录文件中的人名的词库了，快快导入你的rime中吧！