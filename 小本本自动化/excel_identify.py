import openpyxl
import tkinter as tk
from tkinter import filedialog

def read_excel_and_generate_txt(input_file, output_file):
    workbook = openpyxl.load_workbook(input_file)
    sheet = workbook.active

    with open(output_file, 'w', encoding='utf-8') as output_txt:
        groups = {}  # 用于存储相同行的分组

        for row in sheet.iter_rows(min_row=2, values_only=True):
            category = row[0]
            course_name = row[1]
            teacher_name = row[2]
            course_evaluation = row[3]

            key = (category, course_name, teacher_name)
            if key not in groups:
                groups[key] = []
            
            if course_evaluation:
                groups[key].append(course_evaluation)

        for key, evaluations in groups.items():
            category, course_name, teacher_name = key

            if category == '吐槽':
                output_txt.write(f"\\section{{{course_name}}}\n")
                output_txt.write(f"\\subsection{{{teacher_name}}}\n")
                output_txt.write("\\begin{itemize}\n")
                output_txt.write("  \\item \\textcolor{second}{\\textbf{吐槽}}\n")
            elif category == '推荐':
                output_txt.write(f"\\section{{{course_name}}}\n")
                output_txt.write(f"\\subsection{{{teacher_name}}}\n")
                output_txt.write("\\begin{itemize}\n")
                output_txt.write("  \\item \\textcolor{main}{\\textbf{推荐}}\n")

            if evaluations:
                output_txt.write("  \\begin{itemize}\n")
                for evaluation in evaluations:
                    output_txt.write(f"    \\item {evaluation}\n")
                output_txt.write("  \\end{itemize}\n")
                
            output_txt.write("\\end{itemize}\n\n")

def select_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        output_file_path = file_path.replace('.xlsx', '.txt')
        read_excel_and_generate_txt(file_path, output_file_path)
        status_label.config(text=f"生成成功！保存在：{output_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Excel处理程序")

    select_button = tk.Button(root, text="选择Excel文件", command=select_excel_file)
    select_button.pack(pady=20)

    status_label = tk.Label(root, text="", fg="green")
    status_label.pack(pady=10)

    root.mainloop()
