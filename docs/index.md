---
layout: home

hero:
  name: "Rimetool"
  text: "医键通词库转换工具"
  tagline: 一款强大且易用的 Rime 输入法词库转换工具
  actions:
    - theme: brand
      text: 快速开始
      link: /quickstart
    - theme: alt
      text: 在线使用
      link: /web-tool
    - theme: alt
      text: GitHub
      link: https://github.com/B-Beginner/rimetool

features:
  - icon: 🚀
    title: 多格式支持
    details: 支持 VCF 联系人、搜狗词库、简单英文/中文词库、EPUB 电子书等多种格式转换
  - icon: 🌐
    title: Web 在线工具
    details: 提供友好的 Web 界面，无需安装即可在线使用，支持文件上传和下载
  - icon: ⚡
    title: 命令行工具
    details: 提供强大的命令行接口，支持批量处理和自动化脚本集成
  - icon: 🛠️
    title: 易于扩展
    details: 模块化设计，易于添加新的转换格式和功能扩展
  - icon: 📱
    title: 跨平台
    details: 支持 Windows、macOS、Linux 等多个操作系统
  - icon: 🔧
    title: 开源免费
    details: 完全开源，MIT 许可证，永久免费使用
---
## 立即开始

### 🌐 Web 在线工具（推荐）

访问在线工具，无需安装即可使用：

<div style="text-align: left; margin: 2rem 0;">
<a href="/quickstart">立即使用 Web 工具 →</a>
</div>

### 📦 安装使用

```bash
# 通过 pip 安装
pip install rimetool

# 使用命令行工具
rimetool --input-path 你的文件路径 --tool vcf

# 或者使用 Web 界面
python -m rimetool.rimetool_gui.new_app
```

### 🔗 Docker 部署

```bash
# 拉取镜像
docker pull your-registry/rimetool:latest

# 运行容器
docker run -p 5001:5001 your-registry/rimetool:latest
```

## 主要功能

| 工具命令           | 功能描述                             |
| ------------------ | ------------------------------------ |
| `vcf`            | 将联系人文件（.vcf）转换为 Rime 词库 |
| `simple-english` | 将英文单词文件转换为 Rime 词库       |
| `simple-chinese` | 将中文词组文件转换为 Rime 词库       |
| `tosougou`       | 将 Rime 词库转换为搜狗 TXT 词库      |
| `epub`           | 将 EPUB 电子书转换为 Rime 词库       |

## 快速示例

```bash
# 转换联系人文件
rimetool --input-path contacts.vcf --tool vcf

# 转换英文词库
rimetool --input-path english_words.txt --tool simple-english

# 转换中文词库
rimetool --input-path chinese_words.txt --tool simple-chinese

# Rime 转搜狗格式
rimetool --input-path rime_dict.yaml --tool tosougou

# 转换 EPUB 电子书
rimetool --input-path book.epub --tool epub
```

---

<div style="text-align: center; margin: 2rem 0;">
  <p>如果这个项目对你有帮助，请给我们一个 ⭐</p>
  <p><a href="https://github.com/B-Beginner/rimetool">GitHub 仓库</a> | <a href="/quickstart">快速上手</a> | <a href="/api">API 文档</a></p>
</div>
