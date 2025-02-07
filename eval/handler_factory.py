from collections import defaultdict

handlers = defaultdict(dict)

handlers['humaneval_base'] = """
python ../src/main.py \
    --model_name {model_path} \
    --save_path {output} \
    --task "HumanEval" \
    --prompt_type "Completion" \
    --model_type "Chat" \
    --prompt_prefix 'Please provide a self-contained Python script that solves the following problem in a markdown code block:\n```python\n' \
    --prompt_suffix '\n```\n' \
    --response_prefix '' \
    --response_suffix '\n```\n' \
    --trust_remote_code
"""

handlers['mbpp_instruct'] = """
python ../src/main.py \
    --model_name {model_path} \
    --save_path {output} \
    --task "MBPP" \
    --batch_size 1 \
    --prompt_type "Instruction" \
    --prompt_prefix 'Please refer the given examples and generate a python function for my problem.\nExamples are listed as follows:\n' \
    --prompt_suffix '\n\`\`\`\n' \
    --response_prefix "" \
    --trust_remote_code
"""

handlers['humaneval_plus'] = """
python ../src/main.py \
    --model_name {model_path} \
    --save_path {output} \
    --task "HumanEvalPlus" \
    --batch_size 164 \
    --prompt_type "Completion" \
    --model_type "Chat" \
    --prompt_prefix 'Please continue to complete the function. You are not allowed to modify the given code and do the completion only. Please return all completed function in a codeblock. Here is the given code to do completion:\n```python\n' \
    --trust_remote_code
"""

handlers['mbpp_plus'] = """
python ../src/main.py \
    --model_name {model_path} \
    --save_path {output} \
    --task "MBPPPlus" \
    --batch_size 378 \
    --prompt_type "Instruction" \
    --model_type "Chat" \
    --prompt_prefix "" \
    --prompt_suffix 'Your code:\n' \
    --response_prefix "" \
    --trust_remote_code
"""

handlers['leetcode_instruct'] = """
python ../src/main.py \
    --model_name {model_path} \
    --save_path {output} \
    --task "LeetCode" \
    --batch_size 1 \
    --prompt_type "Instruction" \
    --prompt_suffix "" \
    --trust_remote_code
"""

handlers['bigcode_hard'] = """
python ../src/main.py \
    --model_name {model_path} \
    --save_path {output} \
    --task "BigCodeHard" \
    --batch_size 148 \
    --prompt_type "Instruction" \
    --prompt_prefix 'Please provide a self-contained Python script that solves the following problem in a markdown code block:\n' \
    --prompt_suffix '' \
    --response_prefix '' \
    --response_suffix '\n```\n' \
    --trust_remote_code
"""

handlers['bigcode_bench'] = """
python ../src/main.py \
    --model_name {model_path} \
    --save_path {output} \
    --task "BigCodeBench" \
    --batch_size 1140 \
    --prompt_type "Instruction" \
    --prompt_suffix "" \
    --trust_remote_code
"""