import os.path
import argparse
from llm import LLM
from text_utils import split_into_chunks, format_text_with_hashtag, unified_diff


# Paths to the original and processed files
folder_path = 'inout'
input_file = 'input.txt'
formatted_input_file = 'formatted_input.txt'
output_file = 'output.txt'
diff_file = 'diff.txt'


def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def save_text(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    parser = argparse.ArgumentParser(description="LLM Editor")
    parser.add_argument("--url", help="The URL of the Ollama API server. Default: http://localhost:11434")
    parser.add_argument("--model", help="The name of the model setup to use. Default: karen")
    parser.add_argument("--inline", help="Do not print progress, but only output final diff", action='store_true')

    args = parser.parse_args()

    url = args.url or "http://localhost:11434"
    model_name = args.model or "karen"
    inline = args.inline or False

    llm = LLM(url, model_name)

    # Load text from the original .txt file
    original_text = load_text(os.path.join(folder_path, input_file))

    # Split the text into chunks based on lines that start with a hashtag and format text
    chunks = split_into_chunks(original_text)
    formatted_chunks = [format_text_with_hashtag(chunk) for chunk in chunks]

    # Process each chunk with LLM
    if not inline:
        print(f"Starting to process {len(formatted_chunks)} chunks")
    #processed_chunks = [llm.send_to_llm(chunk) for chunk in formatted_chunks]
    processed_chunks = []
    num_chunks = len(formatted_chunks)
    for i, chunk in enumerate(formatted_chunks):
        processed_chunk = llm.send_to_llm(chunk)
        processed_chunks.append(processed_chunk)
        # Print a progress meter
        if not inline:
            print(f"Progress: [{i + 1} / {num_chunks}] ({((i + 1) / num_chunks) * 100:.2f}% complete)")
    if not inline:
        print("Completed LLM processing")



    # Format output again
    formatted_processed_chunks = [format_text_with_hashtag(chunk) for chunk in processed_chunks]

    # Join the processed chunks back together
    formatted_text = "\n\n".join(formatted_chunks) + "\n"
    processed_text = "\n\n".join(formatted_processed_chunks) + "\n"

    # Run a difflib unified difference on the original and processed text
    diff_result = unified_diff(formatted_text, processed_text)+'\n'

    #  Save the files
    save_text(os.path.join(folder_path, formatted_input_file), formatted_text)
    save_text(os.path.join(folder_path, output_file), processed_text)
    save_text(os.path.join(folder_path, diff_file), diff_result)

    # Print the diff result
    if inline:
        print(diff_result)
    else:
        print(f"Written output files to {folder_path}")


if __name__ == "__main__":
    main()
