import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import re

class CodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("代码生成工具")
        self.root.geometry("350x400")

        self.choice_button = tk.Button(root, text="选择题", command=self.open_choice_window, bg="lightblue")
        self.choice_button.pack(fill=tk.BOTH, expand=True)

        self.solution_button = tk.Button(root, text="解析", command=self.open_solution_window, bg="lightgreen")
        self.solution_button.pack(fill=tk.BOTH, expand=True)

        self.note_button = tk.Button(root, text="笔记", command=self.open_note_window, bg="lightyellow")
        self.note_button.pack(fill=tk.BOTH, expand=True)

        self.exercise_button = tk.Button(root, text="填空题", command=self.open_exercise_window, bg="lightpink")
        self.exercise_button.pack(fill=tk.BOTH, expand=True)

        self.dati_button = tk.Button(root, text="应用题 and 计算题", command=self.open_dati_window, bg="lightblue")
        self.dati_button.pack(fill=tk.BOTH, expand=True)

# 选择题格式模板
    def generate_choice_code(self, options, question, answer, option_a, option_b, option_c, option_d):
        template = f"""
\\begin{{example}}{{({options}分)}}
    {question}\\ \\ans{{{answer}}}
    \\begin{{tasks}}(4)
        \\task {option_a}
        \\task {option_b}
        \\task {option_c}
        \\task {option_d}
    \\end{{tasks}}
\\end{{example}}
        """
        return template

# 解析格式模板
    def generate_solution_code(self, solution):
        template = f"""
\\begin{{jiexi}}
    {solution}
\\end{{jiexi}}
        """
        return template

# 笔记格式模板
    def generate_note_code(self, note):
        template = f"""
\\begin{{marker}}
    {note}
\\end{{marker}}
        """
        return template

# 填空题格式模板
    def generate_exercise_code(self, options, knowledge, question, answer):
        template = f"""
\\begin{{example}}{{({options}分)}}{{{knowledge}}}
    {question} \\ \\ans{{{answer}}}.
\\end{{example}}
        """
        return template

# 应用题与计算题格式模板
    def generate_dati_code(self, options, question):
        template = f"""
\\begin{{example}}{{({options}分)}}
    {question}.
\\end{{example}}
        """
        return template




# 格式化输入，将代码内的非中文内容使用$$包裹起来
# 将input_text中的每一个\int前面都加上\displaystyle
# 将input_text中的每一个\frac都改为\dfrac
# 规范化导数的表示为\prime
# 规范化d(全微分)和e(自然对数)的写法
# 规范化各种括号的书写
# 格式化带圈数字的格式
    def process_input(self, input_text):
        processed_text = ""
        i = 0
        while i < len(input_text):
            if not ('\u4e00' <= input_text[i] <= '\u9fff'):  # Check if character is non-Chinese
                j = i + 1
                while j < len(input_text) and not ('\u4e00' <= input_text[j] <= '\u9fff'):
                    j += 1
                processed_text += f"${input_text[i:j]}$"
                i = j
            else:
                processed_text += input_text[i]
                i += 1

        pattern_ed = r"(?<!\\)([de]|d(x|y|z))"  # 匹配非转义的独立字母d和e，或者单独的dx、dy、dz
        processed_text = re.sub(pattern_ed, r"\\mathrm{\1}", processed_text)

        pattern_2 = r"(?<!\\)([()\[\]])"  # 匹配非转义的符号 ( [  ) ]
        processed_text = re.sub(pattern_2, lambda x: x.group(1) if "\\" in x.group(1) else f"\\left{x.group(1)}", processed_text)

        pattern_3 = r"\\textcircled\{(\d+)\}" #更改圈数字的格式
        processed_text = re.sub(pattern_3, lambda x: r"\ding{" + str(int(x.group(1)) + 191) + r"}" if int(x.group(1)) <= 10 else x.group(0), processed_text)

        processed_text = processed_text.replace(r"\int", r"\displaystyle\int")
        processed_text = processed_text.replace(r"\frac", r"\dfrac")

        processed_text = processed_text.replace(r"^{'''}", r"^{\prime\prime\prime}")
        processed_text = processed_text.replace(r"^{''}", r"^{\prime\prime}")
        processed_text = processed_text.replace(r"^{'}", r"^{\prime}")
        processed_text = processed_text.replace(r"'''", r"^{\prime\prime\prime}")
        processed_text = processed_text.replace(r"''", r"^{\prime\prime}")
        processed_text = processed_text.replace(r"'", r"^{\prime}")

        return processed_text

    def open_choice_window(self):
        choice_window = tk.Toplevel(self.root)
        choice_window.title("选择题 输入")
        choice_window.geometry("600x450")

        options_label = tk.Label(choice_window, text="分值：")
        options_label.pack()
        options_entry = tk.Entry(choice_window)
        options_entry.pack()

        timu_label = tk.Label(choice_window, text="题干：")
        timu_label.pack()
        timu_entry = tk.Entry(choice_window, width=60)  # 使用 tk.Text 创建多行文本框
        timu_entry.pack()


        answer_label = tk.Label(choice_window, text="答案：")
        answer_label.pack()
        answer_entry = tk.Entry(choice_window)
        answer_entry.pack()

        option_a_label = tk.Label(choice_window, text="选项A：")
        option_a_label.pack()
        option_a_entry = tk.Entry(choice_window)
        option_a_entry.pack()

        option_b_label = tk.Label(choice_window, text="选项B：")
        option_b_label.pack()
        option_b_entry = tk.Entry(choice_window)
        option_b_entry.pack()

        option_c_label = tk.Label(choice_window, text="选项C：")
        option_c_label.pack()
        option_c_entry = tk.Entry(choice_window)
        option_c_entry.pack()

        option_d_label = tk.Label(choice_window, text="选项D：")
        option_d_label.pack()
        option_d_entry = tk.Entry(choice_window)
        option_d_entry.pack()

        generate_button = tk.Button(choice_window, text="生成", command=lambda: self.show_generated_code(
            self.generate_choice_code(
                self.process_input(options_entry.get()),
                self.process_input(timu_entry.get()),
                self.process_input(answer_entry.get()),
                self.process_input(option_a_entry.get()),
                self.process_input(option_b_entry.get()),
                self.process_input(option_c_entry.get()),
                self.process_input(option_d_entry.get())
            )
        ))
        generate_button.pack()

    def open_solution_window(self):
        solution_window = tk.Toplevel(self.root)
        solution_window.title("解析 输入")
        solution_window.geometry("600x250")

        options_label = tk.Label(solution_window, text="解析内容：")
        options_label.pack()
        options_entry = tk.Entry(solution_window)
        options_entry.pack()

        generate_button = tk.Button(solution_window, text="生成", command=lambda: self.show_generated_code(
            self.generate_solution_code(
                self.process_input(options_entry.get())
            )
        ))
        generate_button.pack()

    def open_note_window(self):
        note_window = tk.Toplevel(self.root)
        note_window.title("笔记 输入")
        note_window.geometry("600x250")

        options_label = tk.Label(note_window, text="笔记内容：")
        options_label.pack()
        options_entry = tk.Entry(note_window)
        options_entry.pack()

        generate_button = tk.Button(note_window, text="生成", command=lambda: self.show_generated_code(
            self.generate_note_code(
                self.process_input(options_entry.get())
            )
        ))
        generate_button.pack()

    def open_exercise_window(self):
        exercise_window = tk.Toplevel(self.root)
        exercise_window.title("解答题 输入")
        exercise_window.geometry("600x250")

        options_label = tk.Label(exercise_window, text="分数：")
        options_label.pack()
        options_entry = tk.Entry(exercise_window)
        options_entry.pack()

        knowledge_label = tk.Label(exercise_window, text="知识点：")
        knowledge_label.pack()
        knowledge_entry = tk.Entry(exercise_window)
        knowledge_entry.pack()

        question_label = tk.Label(exercise_window, text="解答题题干：")
        question_label.pack()
        question_entry = tk.Entry(exercise_window)
        question_entry.pack()

        option_a_label = tk.Label(exercise_window, text="答案：")
        option_a_label.pack()
        option_a_entry = tk.Entry(exercise_window)
        option_a_entry.pack()

        generate_button = tk.Button(exercise_window, text="生成", command=lambda: self.show_generated_code(
            self.generate_exercise_code(
                self.process_input(options_entry.get()),
                self.process_input(knowledge_entry.get()),
                self.process_input(question_entry.get()),
                self.process_input(option_a_entry.get())
            )
        ))
        generate_button.pack()

    def open_dati_window(self):
        dati_window = tk.Toplevel(self.root)
        dati_window.title("应用题 输入")
        dati_window.geometry("600x250")

        options_label = tk.Label(dati_window, text="分值：")
        options_label.pack()
        options_entry = tk.Entry(dati_window)
        options_entry.pack()

        ti_label = tk.Label(dati_window, text="题干：")
        ti_label.pack()
        ti_entry = tk.Entry(dati_window)
        ti_entry.pack()


        generate_button = tk.Button(dati_window, text="生成", command=lambda: self.show_generated_code(
            self.generate_dati_code(
                self.process_input(options_entry.get()),
                self.process_input(ti_entry.get())
            )
        ))
        generate_button.pack()

    def show_generated_code(self, generated_code):
        code_window = tk.Toplevel(self.root)
        code_window.title("生成的代码")

        code_text = scrolledtext.ScrolledText(code_window, wrap=tk.WORD, width=80, height=20)
        code_text.insert(tk.END, generated_code)
        code_text.pack()

        copy_button = tk.Button(code_window, text="复制", command=lambda: self.copy_to_clipboard(code_text.get("1.0", tk.END)))
        copy_button.pack()

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()
