import os
import tkinter as tk
import subprocess
from PIL import Image, ImageTk  # 导入PIL库

# 获取当前脚本所在的目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))

def call_add_period():
    subprocess.run(["python", os.path.join(current_dir, "add_period.py")])

def call_sort_file():
    subprocess.run(["python", os.path.join(current_dir, "sort_file.py")])

def call_excel_identify():
    subprocess.run(["python", os.path.join(current_dir, "excel_identify.py")])

def show_image(image_path):
    image = Image.open(image_path)
    image.show()  # 使用系统默认的图片查看器显示图片

# Create the GUI
root = tk.Tk()
root.title("摸鱼子的摸鱼工具")  # 修改窗口标题

# 设置窗口大小和位置
window_width = 300
window_height = 200
window_horizontal_offset = 100
window_vertical_offset = 100
root.geometry(f"{window_width}x{window_height}+{window_horizontal_offset}+{window_vertical_offset}")

# 定义按钮颜色
button_colors = ['#FF5722', '#4CAF50', '#2196F3']

# 添加功能按钮，并设置不同颜色和中文文字
add_period_button = tk.Button(root, text="添加句号", command=call_add_period, bg=button_colors[0], fg='white')
add_period_button.grid(row=0, column=0, padx=20, pady=10)

sort_button = tk.Button(root, text="排序文件", command=call_sort_file, bg=button_colors[1], fg='white')
sort_button.grid(row=1, column=0, padx=20, pady=10)

excel_identify_button = tk.Button(root, text="Excel处理", command=call_excel_identify, bg=button_colors[2], fg='white')
excel_identify_button.grid(row=2, column=0, padx=20, pady=10)

def show_add_period_image():
    show_image("106245804_p0.jpg")

def show_sort_file_image():
    show_image("106245804_p0.jpg")

def show_excel_identify_image():
    show_image("106245804_p0.jpg")

# 添加图片显示按钮，并设置中文文字
show_add_period_image_button = tk.Button(root, text="查看添加句号说明", command=show_add_period_image, fg='blue', cursor='hand2')
show_add_period_image_button.grid(row=0, column=1, padx=20, pady=10)

show_sort_file_image_button = tk.Button(root, text="查看排序文件说明", command=show_sort_file_image, fg='blue', cursor='hand2')
show_sort_file_image_button.grid(row=1, column=1, padx=20, pady=10)

show_excel_identify_image_button = tk.Button(root, text="查看Excel处理说明", command=show_excel_identify_image, fg='blue', cursor='hand2')
show_excel_identify_image_button.grid(row=2, column=1, padx=20, pady=10)

root.mainloop()
