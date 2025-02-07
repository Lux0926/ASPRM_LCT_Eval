import os


def to_eval_dir(path, sft_job):
    keyword = sft_job.split('/')[-1]
    eval_path =  path.replace(keyword, 'evaluation', 1)
    if not os.path.exists(eval_path):
        os.makedirs(eval_path)
    return eval_path


def to_handler_dir(path, handler):
    handler_path = os.path.join(path, handler)
    if not os.path.exists(handler_path):
        os.makedirs(handler_path)
    return handler_path