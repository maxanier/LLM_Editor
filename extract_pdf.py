from pdftext.extraction import plain_text_output
from src.text_utils import fix_broken_tex_output
import os.path
import argparse

def save_text(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    parser = argparse.ArgumentParser(description="Extract Text from a PDF as good as possible.")
    parser.add_argument("--input", help="Input file. Defaults to 'inout/input.pdf'")
    parser.add_argument("--output", help="Output file. Defaults to `inout/input.txt`")

    args = parser.parse_args()

    input_file = args.input or "inout/input.pdf"
    output_file = args.output or "inout/input.txt"

    text = plain_text_output(input_file, sort=False, hyphens=False)
    text = fix_broken_tex_output(text)

    save_text(output_file, text)



if __name__ == "__main__":
    main()
