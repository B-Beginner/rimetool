# 安装

Rimetool 提供多种安装方式，你可以根据自己的需求选择合适的方法。

## 方式一：通过 pip 安装（推荐）

这是最简单的安装方式：

```bash
pip install rimetool
```

安装完成后，你可以直接在命令行中使用 `rimetool` 命令。

## 方式二：从源码安装

如果你想使用最新的开发版本或者参与开发，可以从源码安装：

```bash
# 克隆仓库
git clone https://github.com/B-Beginner/rimetool.git
cd rimetool

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

## 方式三：Docker 部署

适用于想要部署 Web 服务的用户：

```bash
# 使用官方镜像
docker pull your-registry/rimetool:latest

# 运行容器
docker run -d -p 5001:5001 --name rimetool your-registry/rimetool:latest
```

或者从源码构建：

```bash
# 克隆仓库
git clone https://github.com/B-Beginner/rimetool.git
cd rimetool

# 构建镜像
docker build -t rimetool .

# 运行容器
docker run -d -p 5001:5001 --name rimetool rimetool
```

## 验证安装

安装完成后，可以通过以下命令验证安装是否成功：

```bash
# 查看版本
rimetool --version

# 查看帮助
rimetool --help
```

## 系统要求

- **Python**: 3.0 或更高版本
- **操作系统**: Windows, macOS, Linux
- **内存**: 建议 512MB 以上
- **存储**: 50MB 可用空间

## 依赖包

Rimetool 依赖以下 Python 包：

- `pypinyin` - 中文拼音转换
- `argparse` - 命令行参数解析
- `click` - 命令行界面构建
- `chardet` - 字符编码检测
- `flask` - Web 框架（仅 Web 版本需要）
- `flask-cors` - 跨域资源共享（仅 Web 版本需要）

这些依赖会在安装时自动安装。

## 可能的问题

### 权限问题

如果在安装时遇到权限问题，可以尝试：

```bash
# 使用用户安装
pip install --user rimetool

# 或者使用 sudo（Linux/macOS）
sudo pip install rimetool
```

### 网络问题

如果下载速度较慢，可以使用国内镜像：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple rimetool
```

### Python 版本问题

确保你的 Python 版本满足要求：

```bash
python --version
```

如果版本过低，请升级 Python 到 3.0 或更高版本。

## 下一步

安装完成后，你可以：

- [查看快速上手指南](/quickstart)
- [了解所有支持的功能](/cli)
- [使用 Web 在线工具](/web-tool)