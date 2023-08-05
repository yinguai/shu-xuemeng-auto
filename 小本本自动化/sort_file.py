import re

def sort_subsection_within_section(content):
    # 定义一个正则表达式模式，用于匹配每个section的内容
    section_pattern = r'\\section{([^}]*)}([\s\S]*?)(?=\\section|\\newpage|$)'

    # 使用正则表达式提取所有section块及其内容
    sections = re.findall(section_pattern, content)

    # 对每个section的内容进行处理
    sorted_content = ''
    for i, section in enumerate(sections):
        section_title = section[0]
        subsection_content = section[1]
        sorted_subsection_content = sort_subsection(subsection_content)  # 调用之前的排序函数

        # 在每个section之前添加\newpage，并在第一个section之前不添加
        if i > 0:
            sorted_content += '\\newpage\n'
        sorted_content += f'\\section{{{section_title}}}\n{sorted_subsection_content}\n\n'

    return sorted_content

def sort_subsection(content):
    # 定义一个正则表达式模式，用于匹配`\subsection{}`及其内容
    subsection_pattern = r'\\subsection{([^}]*)}([\s\S]*?)(?=\\subsection|$)'

    # 使用正则表达式提取所有`\subsection{}`块及其内容
    subsections = re.findall(subsection_pattern, content)

    # 根据内容（正则表达式中的第一个组）对`\subsection{}`进行排序
    sorted_subsections = sorted(subsections, key=lambda x: x[0])

    # 按顺序组合排序后的`\subsection{}`块，形成排序后的内容
    sorted_content = ''
    for i, subsection in enumerate(sorted_subsections):
        sorted_content += f'\\subsection{{{subsection[0]}}}{subsection[1]}'
        # 在每个`\subsection{}`之间留出两行空白
        if i < len(sorted_subsections) - 1:
            sorted_content += '\n\n\n'

    return sorted_content

if __name__ == "__main__":
    input_file_path = input("请输入输入文件的路径：")
    output_file_path = input("请输入输出文件的路径：")

    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取chapter内容并保存
    chapter_pattern = r'\\chapter{([^}]*)}'
    chapter = re.findall(chapter_pattern, content)
    sorted_content = f'\\chapter{{{chapter[0]}}}\n\n'

    # 处理section和subsection内容
    sorted_content += sort_subsection_within_section(content)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(sorted_content)

    print("排序并移动\\subsection{}完成。结果已写入输出文件。")
