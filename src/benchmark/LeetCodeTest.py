import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([os.path.dirname(ROOT), os.path.dirname(os.path.dirname(ROOT))])

from benchmark.base import Benchmark
from sanitize import sanitize
from eval.execution import check_correctness
from utils import refine_text, stream_jsonl, python_extract

class LeetCodeTest(Benchmark):

    name: str = "LeetCodeTest"

    train_path = os.path.abspath(os.path.join(ROOT, "../data/1745_leetcode_problems_train.jsonl"))
    test_path = os.path.abspath(os.path.join(ROOT, "../data/1745_leetcode_problems_test.jsonl"))

    general_stop_words = [
                            "<｜end▁of▁sentence｜>"
                        ]
    
    completion_stop_words = []

    def __init__(self,
                 name: str = "LeetCodeTest",
                 timeout = 3.0,
                 prompt_type = "Instruction"): 
        super().__init__()
        
        self.name = name
        self.timeout = timeout
        self.prompt_type = prompt_type

        if self.name == "LeetCodeTrain":
            self.path = self.train_path
        elif self.name == "LeetCodeTest":
            self.path = self.test_path
    
        self.tasks = self.get_task()

    def get_task(self):
        """
        Get the task data from the jsonl file into a dictionary.
        """

        tasks = {}
        
        for task_data in stream_jsonl(filename=self.path):

            task_id = int(task_data["meta"]["question_id"])
            tasks[task_id] = task_data
        
        return tasks
        
    def get_prompt(self):
        """
        Builds the prompt for the LM to generate from.
        """

        prompts = []
        for task_id, task_data in self.tasks.items():

            prompts.append(
                dict(
                    task_id = task_id,
                    prompt = refine_text(task_data['meta']['en_src'])
                )
            )

        return prompts

    def postprocess_generation(self, generation):
        """
        Postprocess the generations.
        """

        return dict(
            task_id = generation['task_id'],
            completion_id = generation['completion_id'],
            solution = python_extract(generation['completion'])
        )
    
    def process_results(self, solution):
        """
        Takes the list of LM generations and evaluates them against the test cases
        """

        task_data = self.tasks[solution['task_id']]

        code = (
                    task_data['prompt'] + "\n"
                    + task_data['meta']['lang_code'] + "\n"
                    + "        pass\n" + "\n"
                    + solution['solution'] + "\n"
                    + task_data['test'] + "\n"
                    + f"check({task_data['entry_point']})"
                )

        # import time
        # print(code)
        # time.sleep(10)
        result = check_correctness(solution['task_id'],
                                   solution['completion_id'],
                                   code,
                                   self.timeout)
        
        return result