import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess

"""
gui雏形：方便医学组同学，点击按钮选择文件输入输出路径，并且选择参数，点击运行按钮，运行命令行指令。
"""

def run_command():
    # 获取用户选择的输入路径、输出路径和参数
    input_path = input_var.get()
    output_path = output_var.get()
    param = param_var.get()

    # 这里可以根据你的实际需求修改命令行指令
    command = f"python your_script.py --input {input_path} --output {output_path} --param {param}"

    try:
        # 执行命令行指令
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        messagebox.showinfo("执行结果", f"命令执行成功！\n输出信息：{result.stdout}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("执行错误", f"命令执行失败！\n错误信息：{e.stderr}")

def select_input_path():
    path = filedialog.askdirectory()
    if path:
        input_var.set(path)

def select_output_path():
    path = filedialog.askdirectory()
    if path:
        output_var.set(path)

# 创建主窗口
root = tk.Tk()
root.title("命令行指令打包 GUI")
root.geometry("400x300")  # 设置窗口初始大小
root.configure(bg="#f0f0f0")  # 设置窗口背景颜色

# 创建样式
style = ttk.Style()
style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
style.configure("TButton", background="#007acc", foreground="white", font=("Arial", 12))
style.configure("TEntry", fieldbackground="white", font=("Arial", 12))
style.configure("TCombobox", selectbackground="#007acc", selectforeground="white", font=("Arial", 12))

# 创建输入路径选择部分
input_label = ttk.Label(root, text="输入路径:")
input_label.pack(pady=10)

input_var = tk.StringVar()
input_entry = ttk.Entry(root, textvariable=input_var, width=30)
input_entry.pack(pady=5)

input_button = ttk.Button(root, text="选择输入路径", command=select_input_path)
input_button.pack(pady=5)

# 创建输出路径选择部分
output_label = ttk.Label(root, text="输出路径:")
output_label.pack(pady=10)

output_var = tk.StringVar()
output_entry = ttk.Entry(root, textvariable=output_var, width=30)
output_entry.pack(pady=5)

output_button = ttk.Button(root, text="选择输出路径", command=select_output_path)
output_button.pack(pady=5)

# 创建参数选择部分
param_label = ttk.Label(root, text="选择参数:")
param_label.pack(pady=10)

param_var = tk.StringVar()
param_var.set("参数 1")  # 默认选择
param_options = ["参数 1", "参数 2", "参数 3"]
param_menu = ttk.Combobox(root, textvariable=param_var, values=param_options)
param_menu.pack(pady=5)

# 创建运行按钮
run_button = ttk.Button(root, text="运行命令", command=run_command)
run_button.pack(pady=15)

# 运行主循环
root.mainloop()