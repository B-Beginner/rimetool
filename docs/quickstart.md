# 快速上手

本指南将帮助你快速上手 Rimetool，了解基本用法和主要功能。

## 前提条件

确保你已经[安装了 Rimetool](/install)。

## 基本概念

Rimetool 是一个专为 Rime 输入法设计的词库转换工具，它可以：

- 将各种格式的文件转换为 Rime 词库格式
- 将 Rime 词库转换为其他输入法格式
- 提供 Web 界面和命令行两种使用方式

## 命令行基本用法

### 查看帮助

```bash
rimetool --help
```

### 基本命令格式

```bash
rimetool --input-path <输入文件> --tool <转换工具> [--output-path <输出目录>]
```

## 常用转换示例

### 1. 转换联系人文件

将手机联系人文件（VCF 格式）转换为 Rime 词库：

```bash
rimetool --input-path contacts.vcf --tool vcf
```

这会生成一个包含联系人姓名的 Rime 词库文件。

### 2. 转换英文词库

将英文单词列表转换为 Rime 词库：

```bash
# 输入文件内容示例（每行一个单词）:
# hello
# world
# programming

rimetool --input-path english_words.txt --tool simple-english
```

### 3. 转换中文词库

将中文词组转换为 Rime 词库：

```bash
# 输入文件内容示例（每行一个词组）:
# 你好
# 世界
# 编程

rimetool --input-path chinese_words.txt --tool simple-chinese
```

### 4. Rime 转搜狗格式

将 Rime 词库转换为搜狗输入法格式：

```bash
rimetool --input-path my_dict.yaml --tool tosougou
```

### 5. 转换 EPUB 电子书

从 EPUB 电子书中提取文本并生成词库：

```bash
rimetool --input-path book.epub --tool epub
```

## Web 界面使用

### 启动 Web 服务

如果你想使用图形界面，可以启动 Web 服务：

```bash
python -m rimetool.rimetool_gui.new_app
```

然后在浏览器中访问 `http://localhost:5001`。

### Web 界面功能

- **文件上传**: 拖拽或点击上传要转换的文件
- **格式选择**: 选择对应的转换工具
- **实时进度**: 查看转换进度和日志
- **文件下载**: 转换完成后直接下载结果文件

## 输出文件

### 文件命名规则

转换后的文件会按照以下规则命名：

```
{工具名}_output.dict_{时间戳}.yaml
```

例如：
- `simple_english_output.dict_2024-01-15_14-30-25.yaml`
- `vcf_output.dict_2024-01-15_14-30-25.yaml`

### 输出目录

默认情况下，输出文件会保存在当前目录下。你可以通过 `--output-path` 参数指定输出目录：

```bash
rimetool --input-path input.txt --tool simple-english --output-path ./output/
```

## 常见问题

### 1. 文件编码问题

如果输入文件包含中文，请确保文件编码为 UTF-8。Rimetool 会自动检测常见编码格式。

### 2. 文件格式要求

不同的转换工具对输入文件格式有不同要求：

- **vcf**: 标准 VCF 联系人格式
- **simple-english/simple-chinese**: 纯文本，每行一个词
- **tosougou**: Rime 词库 YAML 格式
- **epub**: 标准 EPUB 电子书格式

### 3. 权限问题

如果遇到文件读写权限问题，请确保：
- 输入文件可读
- 输出目录可写
- 程序有足够的权限

## 下一步

现在你已经掌握了 Rimetool 的基本用法，可以：

- [了解所有支持的格式](/formats)
- [探索 Web 在线工具](/web-tool)
- [查看 API 文档](/api)
- [学习自定义转换](/custom)