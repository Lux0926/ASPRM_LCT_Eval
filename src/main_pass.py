import os
import argparse
import re

os.environ["TOKENIZERS_PARALLELISM"] = "false"

import numpy as np

from args import get_args, check_args
from utils import refine_text, write_jsonl, group_and_count, estimate_pass_at_k, stream_jsonl

from backend.vllm import VllmGenerator
from factory import BenchmarkFactory


from tqdm import tqdm
from typing import Callable, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

def multi_process_function(function: Callable,
                           parameters: List,
                           num_workers: int = 1,
                           desc: str = "Completing tasks"):
    
    if num_workers > len(parameters) or num_workers > os.cpu_count():
        num_workers = min(os.cpu_count(), len(parameters))

    with ThreadPoolExecutor(num_workers) as executor:
        futures = []
        for param in parameters:
            future = executor.submit(function, param)
            futures.append(future)
            
        results = []
        for future in tqdm(as_completed(futures), total=len(futures), desc=desc):
            result = future.result()
            results.append(result)

    return results

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    args = get_args(parser)
    args = check_args(args)

    save_path = args.save_path
    input_file = args.input_file
    output_file = args.output_file
    eval_type = args.eval_type
    pass_size = args.pass_size
    os.makedirs(save_path, exist_ok=True)

    task = BenchmarkFactory.get_task(args)

    file_path = input_file

    data_list = []

    if args.task == "LeetCodeTest":
        target_path = '/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/oce_new_v2/src/data/1745_leetcode_problems_test.jsonl'
    if args.task == "LeetCodeTrain":
        target_path = "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/oce_new_v2/src/data/1745_leetcode_problems_train.jsonl"
    task_question_list = []

    with open(target_path, 'r') as f:
        for line in f:
            # 使用 json.loads() 解析每一行的 JSON 数据
            obj = json.loads(line.strip())
            
            # 提取 task_id 和 meta.question_id
            task_id = obj.get('task_id')  # 获取 task_id
            question_id = obj.get('meta', {}).get('question_id')  # 获取 meta 中的 question_id
            
            # 如果 task_id 和 question_id 存在，保存到列表中
            if task_id is not None and question_id is not None:
                task_question_list.append({'task_id': task_id, 'question_id': question_id})

    task_id_to_question_id = {item['task_id']: item['question_id'] for item in task_question_list}
    
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            data_list.append(data)

    all_score = 0
    for data in data_list:
        question_id = task_id_to_question_id.get(data["task_id"])

        answer_list = data["pred"]
        pass_list = answer_list[:pass_size]
        pass_score = 0
        for pass_answer in pass_list:
            generations = [{
                # 'task_id': data["task_id"],
                'task_id': question_id,
                'completion_id': 1,
                'completion': pass_answer
            }]

            solutions = multi_process_function(function = task.postprocess_generation,
                                            parameters = generations,
                                            num_workers = args.num_workers,
                                            desc = "Post-processing solutions")
            # print(solutions)

            write_jsonl(save_path + "/solutions.jsonl", solutions)

            evaluations = multi_process_function(function = task.process_results,
                                                    parameters = solutions,
                                                    num_workers = args.num_workers,
                                                    desc = "Evaluating solutions")
            print(evaluations)
            # import time
            # time.sleep(4)
            with open(output_file, "a", encoding="utf-8") as of:
        
                json.dump(evaluations[0], of, ensure_ascii=False)

                of.write("\n")

            if evaluations[0]["passed"] == True:
                pass_score = 1
        if pass_score == 1:
            all_score = all_score+1

    pass_final_score = all_score/len(data_list)
    with open("result_pass@n.jsonl", "a", encoding="utf-8") as ff:
        ff.write(input_file+":"+"pass@"+str(pass_size)+":"+str(pass_final_score))
        ff.write("\n")
    print(pass_final_score)
            
        # data["final_eval_score"] = final_eval_score

        # with open(output_file, 'a', encoding="utf-8") as f:
        #     json.dump(data, f, ensure_ascii=False)
        #     f.write('\n')



