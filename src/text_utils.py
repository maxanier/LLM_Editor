import difflib
import re


def split_into_chunks(text):
    # Split the text into chunks based on lines that start with a hashtag
    if not '#' in text:
        return [text]
    chunks = re.split(r'(?m)^#', text)
    return ["#" + chunk for chunk in chunks if chunk.strip()]

def split_at_paragraph_breaks(text):
    # Split the text by one or more empty lines
    paragraphs = text.split('\n\n')
    paragraphs = [paragraph for paragraph in paragraphs if paragraph.strip()] # Remove empty ones
    return paragraphs

def split_long_chunks_at_paragraphs(chunk_list, max_chars=1000):
    result_list = []
    for string in chunk_list:
        if len(string) > max_chars:
            # Split the string at paragraph breaks
            paragraphs = split_at_paragraph_breaks(string)
            # Add each paragraph to the result list
            result_list.extend(paragraphs)
        else:
            # If the string is not longer than desired, add it as is
            result_list.append(string)
    return result_list


def format_text_with_hashtag(text_chunk, latex=False):
    # If the chunk starts with a hashtag, preserve the first newline after the hashtag line
    if text_chunk.startswith("#"):
        lines = text_chunk.split('\n', 1)
        if len(lines) > 1:
            # Process the rest of the chunk, but keep the first part (hashtag line) intact
            return clean_and_break_text(lines[1],latex)
        else:
            return ""  # Return the chunk as is if there's no additional content
    # Otherwise, format the entire text chunk
    return clean_and_break_text(text_chunk, latex)


def fix_broken_tex_output(text):
    text = text.replace("??", "Figure 1") # References may be broken when figures are not included in PDF -> Use placeholder
    return text

def clean_and_break_text(text, latex=False):
    if not latex:
        text = text.replace("Fig.", "Figure")
        text = text.replace("i.e.", "that is")
        text = text.replace("e.g.", "for example")
    return format_linebreaks(text, latex)

def format_linebreaks(text, latex=False):

    # Remove arbitrary line breaks
    if not latex:
        text = re.sub(r'\n+', ' ', text)

    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])[ \t]+', text.strip())

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
