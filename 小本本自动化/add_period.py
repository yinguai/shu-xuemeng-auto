import re
import tkinter as tk
from tkinter import filedialog

# 定义需要跳过的\item
skip_items = ["\\item \\textcolor{main}{\\textbf{推荐}}", "\\item \\textcolor{second}{\\textbf{吐槽}}"]

def process_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            modified_content = process_content(content)
        
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(modified_content)
            result_label.config(text="文件处理完成！")
        else:
            result_label.config(text="未选择保存路径！")
    else:
        result_label.config(text="未选择文件！")

def process_content(content):
    pattern = r"(\\subsection{.*?}(.*?)(?=\\subsection|$))"
    matches = re.findall(pattern, content, re.DOTALL)
    if matches:
        for match in matches:
            subsection, itemize = match[0], match[1]
            modified_itemize = process_itemize(itemize)
            content = content.replace(itemize, modified_itemize)
    return content

def process_itemize(itemize_content):
    main_pattern = r"\\textcolor{main}{\\textbf{推荐}}(.*?)(?=\\textcolor{second}{\\textbf{吐槽}}|$)"
    main_matches = re.findall(main_pattern, itemize_content, re.DOTALL)
    if main_matches:
        for main_match in main_matches:
            modified_itemize_content = main_match.strip()
            modified_itemize_content = re.sub(r"(\\item.*?)([^.!?。！？])$", r"\1\2.", modified_itemize_content, flags=re.MULTILINE)
            itemize_content = itemize_content.replace(main_match, modified_itemize_content)
    
    second_pattern = r"\\textcolor{second}{\\textbf{吐槽}}(.*?)$"
    second_matches = re.findall(second_pattern, itemize_content, re.DOTALL)
    if second_matches:
        for second_match in second_matches:
            modified_itemize_content = second_match.strip()
            modified_itemize_content = re.sub(r"(\\item.*?)([^.!?。！？])$", r"\1\2.", modified_itemize_content, flags=re.MULTILINE)
            itemize_content = itemize_content.replace(second_match, modified_itemize_content)
    return itemize_content

# 创建GUI界面
root = tk.Tk()
root.title("自动添加句号")
root.geometry("400x150")

# 添加按钮和标签
process_button = tk.Button(root, text="选择文件并处理", command=process_file)
process_button.pack(pady=20)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
