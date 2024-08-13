# LLM Text Editor
This script sends text chunks to an `ollama` server running the Large Language Model (LLM).
It performs pre- and post-processing and creates a diff between the original text and the edited version.

Not perfect, but helpful.

## Usage
1. You need an [ollama](https://github.com/ollama/ollama/) instance running. Adjust the end-point if necessary
2. Make sure you have to desired model installed
3. Save the text you want to check in `inout/input.txt`. (See `inout/input.example.txt`)
4. If it is a long text, add lines starting with `#` to break the text into chunks. (E.g. preprend headings with `#`)
5. Run script (see `python main.py --help`)
6. e.g. run [diff-so-fancy](https://github.com/so-fancy/diff-so-fancy) on the output diff file (`cat inout/diff.txt | diff-so-fancy`)

## Models
Different models and corresponding system prompts can be configured in `llm_config.json`.
Most concise results are achieved with `karen` so far.