from src.text_utils import fix_broken_tex_output
import os.path
import argparse



import regex as re

regex_caption = r"\\caption\{(?:[^{}] | (?:\{.*\}))*\}"
caption_pattern = re.compile(regex_caption, re.DOTALL | re.X)


def process_figure_content(str):
    g = caption_pattern.search(str)
    return g.group(0) if g else ''

def process_latex_file(input_path):
    # Read the content of the LaTeX file
    with open(input_path, 'r', encoding='utf-8') as file:
        latex_content = file.read()

    # Step 0: Remove comments and todo
    comment_pattern = re.compile(r"%.*$", re.MULTILINE)
    latex_content = comment_pattern.sub('', latex_content)

    todo_pattern = re.compile(r'\\todo(\[.+\])?\{(?:[^{}] | (?:\{.*\}))*\}', re.X)
    latex_content = todo_pattern.sub('', latex_content)

    # Step 1: Remove figures, retaining only the \caption{Text}
    figure_pattern = re.compile(r"\\begin{figure}((?!\\begin{figure}).)*\\end{figure}", re.DOTALL)
    latex_content = figure_pattern.sub(lambda match: process_figure_content(match.group(0)), latex_content)

    # Step 2: Replace section, subsection, and subsubsection commands
    section_pattern = re.compile(r'\\section{(.*?)}')
    subsection_pattern = re.compile(r'\\subsection{(.*?)}')
    subsubsection_pattern = re.compile(r'\\subsubsection{(.*?)}')

    latex_content = section_pattern.sub(r'# \1', latex_content)
    latex_content = subsection_pattern.sub(r'## \1', latex_content)
    latex_content = subsubsection_pattern.sub(r'### \1', latex_content)

    # Step 3: Replace equation environments with <equation>
    equation_pattern = re.compile(r"\\begin\{equation\}((?!\\begin\{equation\}).)*\\end\{equation\}", re.DOTALL)
    latex_content = equation_pattern.sub('<equation>', latex_content)

    # Step 4: Replace non-breaking space ~ with normal space
    latex_content = latex_content.replace('~',' ')

    return latex_content

def save_text(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    parser = argparse.ArgumentParser(description="Extract Text from a LaTeX source file as good as possible.")
    parser.add_argument("--input", help="Input file. Defaults to 'inout/input.tex'")
    parser.add_argument("--output", help="Output file. Defaults to `inout/input.txt`")

    args = parser.parse_args()

    input_file = args.input or "inout/input.tex"
    output_file = args.output or "inout/input.txt"

    text = process_latex_file(input_file)

    save_text(output_file, text)



if __name__ == "__main__":
    main()
