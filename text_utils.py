import difflib
import re


def split_into_chunks(text):
    # Split the text into chunks based on lines that start with a hashtag
    chunks = re.split(r'(?m)^#', text)
    return ["#" + chunk for chunk in chunks if chunk.strip()]


def format_text_with_hashtag(text_chunk):
    # If the chunk starts with a hashtag, preserve the first newline after the hashtag line
    if text_chunk.startswith("#"):
        lines = text_chunk.split('\n', 1)
        if len(lines) > 1:
            # Process the rest of the chunk, but keep the first part (hashtag line) intact
            return format_text(lines[1])
        else:
            return ""  # Return the chunk as is if there's no additional content
    # Otherwise, format the entire text chunk
    return format_text(text_chunk)


def format_text(text):
    # Remove arbitrary line breaks
    text = text.replace("Fig.", "Figure")
    text = re.sub(r'\n+', ' ', text)

    # Split text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text.strip())

    # Join sentences with a newline character
    formatted_text = "\n".join(sentences)

    return formatted_text


def unified_diff(original_text, processed_text):
    diff = difflib.unified_diff(
        original_text.splitlines(),
        processed_text.splitlines(),
        lineterm='',
        fromfile='original.txt',
        tofile='processed.txt'
    )
    return '\n'.join(diff)


def remove_empty_lines(input_string):
    return '\n'.join([line for line in input_string.split('\n') if line.strip()])
