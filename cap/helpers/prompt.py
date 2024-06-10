#!/usr/bin/env python3
from textwrap import dedent


def cleanup_preprompt(preprompt: str, remove_indent: bool = False):
    preprompt = dedent(preprompt)
    lines = preprompt.strip().split('\n')
    processed_lines = []

    # Comment lines start with "###"
    for line in lines:
        if not line.strip() or line.startswith('###'):
            continue

        if remove_indent:
            # NOTE: removing indents harmed the performance...
            processed_lines.append(line.strip())
        else:
            processed_lines.append(line)
    return '\n'.join(processed_lines)


def complete_full(preprompt: str, api_key: str, engine: str = 'text-davinci-003'):
    """Call the OpenAI API to continue the prompt to the limit of its context window"""

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    def call_openai(prompt):
        print('Calling OpenAI API...')
        api_results = client.completions.create(prompt=prompt,
        temperature=0,
        engine=engine,
        max_tokens=-1)
        return api_results.choices[0].text.strip()

    return call_openai(preprompt)


def read_from_file(fpath):
    with open(fpath, 'r') as f:
        text = f.read()
    return text


def load_prompts(search_root_dir=None):
    """Load all prompts from the current directory and `functions` directory.

    Returns:
        dict: name to prompt
    """
    from cap.helpers import rootdir
    # Traverse the directory and find *.txt
    # then create a dictionary that maps prompt name to its content
    if search_root_dir is None:
        search_root_dir = rootdir

    name2prompt = {}
    for path in search_root_dir.glob('**/*.txt'):
        # 'cap_wm_updater/metainfo.txt' -> 'cap_wm_updater.metainfo'
        prompt_name = str(path.relative_to(search_root_dir).parent / path.stem).replace('/', '.')
        name2prompt[prompt_name] = read_from_file(path)

    return {key: cleanup_preprompt(val) for key, val in name2prompt.items()}
