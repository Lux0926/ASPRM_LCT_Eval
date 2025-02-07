import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([os.path.dirname(ROOT), os.path.dirname(os.path.dirname(ROOT))])
import re
import gzip
import json
import itertools
import numpy as np

from typing import Dict, List, Union, Iterable
from collections import defaultdict
from transformers import AutoTokenizer

# def python_extract(text: str) -> str:

#     python_pattern = r'```python\s*\n(.*?)\n\s*```'
#     python_re = re.compile(python_pattern, re.DOTALL | re.IGNORECASE)

#     match = python_re.search(text)
#     if match:
#         return match.group(1)
#     else:
#         return ""

# def python_extract(text: str) -> str:

#     python_re = re.compile(r'```python\s*([\s\S]*?)```')
#     code_block = python_re.search(text)
    
#     if code_block:
#         code = code_block.group(1)
#         return code
#     else:
#         return ""

def python_extract(text: str) -> str:
    python_pattern = r"```python[ \t]*[\r\n]+(.*?)[ \t]*[\r\n]+```"
    python_re = re.compile(python_pattern, re.DOTALL | re.IGNORECASE)

    match = python_re.search(text)
    if match:
        return match.group(1)
    else:
        return ""

def refine_text(text: str) -> str:
    text =  text.replace("\t", "    ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip() + "\n"

def format_test_example(q, tests, code: str=None):
    prompt = ">>> Problem:\n{}\n>>> Test Cases:\n{}\n".format(q.strip(), "\n".join(tests))
    if code:
        code = code.replace("\r", "").replace("\t", "    ")
        prompt += "\n>>> Code:\n```python\n{}\n```".format(code)
    return prompt

def make_chat_prompt(prompt: str,
                     tokenizer: AutoTokenizer,
                     response_prefix: str = ""
                    ) -> str:
    # directly return prompt if it does not have a tokenizer.chat_template

    return '''
You are an AI programming assistant.
### Instruction:
{}
### Response:
'''.format(prompt.strip()).lstrip()

    ckpt_names = [
        "ckpt",
        "checkpoint",
        "ckp",
        "step",
        "final"
    ]

    if tokenizer.chat_template:

        if any(ckpt in tokenizer.name_or_path for ckpt in ckpt_names):

            return '''
You are an AI programming assistant.
### Instruction:
{}
### Response:
'''.format(prompt.strip()).lstrip()
        
        else:
            prompt = tokenizer.apply_chat_template(
            [
                {"role": "user", "content":  prompt},
            ],
            tokenize = False,
            add_generation_prompt = True
        ) + response_prefix
        
    return prompt[len(tokenizer.bos_token):] if prompt.startswith(tokenizer.bos_token) else prompt


def stream_jsonl(filename: str) -> Iterable[Dict]:
    """
    Parses each jsonl line and yields it as a dictionary
    """
    if filename.endswith(".gz"):
        with open(filename, "rb") as gzfp:
            with gzip.open(gzfp, 'rt') as fp:
                for line in fp:
                    if any(not x.isspace() for x in line):
                        yield json.loads(line)
    else:
        with open(filename, "r", encoding="utf-8") as fp:
            for line in fp:
                if any(not x.isspace() for x in line):
                    yield json.loads(line)


def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False):
    """
    Writes an iterable of dictionaries to jsonl
    """
    if append:
        mode = 'ab'
    else:
        mode = 'wb'
    filename = os.path.expanduser(filename)
    if filename.endswith(".gz"):
        with open(filename, mode) as fp:
            with gzip.GzipFile(fileobj=fp, mode='wb') as gzfp:
                for x in data:
                    gzfp.write((json.dumps(x) + "\n").encode('utf-8'))
    else:
        with open(filename, mode) as fp:
            for x in data:
                fp.write((json.dumps(x) + "\n").encode('utf-8'))

def group_and_count(results, group_key, count_key):

    groups = defaultdict(int)
    
    for item in results:
        group_id = item.get(group_key)
        if group_id not in groups:
            groups[group_id] = 0
        if item.get(count_key) == True:
            groups[group_id] += 1
    
    return list(groups.values())

def estimate_pass_at_k(
    num_samples: Union[int, List[int], np.ndarray],
    num_correct: Union[List[int], np.ndarray],
    k: int
) -> np.ndarray:
    """
    Estimates pass@k of each problem and returns them in an array.
    """

    def estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).
        """
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array([estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)])
