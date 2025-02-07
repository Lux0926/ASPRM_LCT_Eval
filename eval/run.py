import os
import re
import sys
import json
import time
import subprocess
from loguru import logger
from collections import defaultdict
from argparse import ArgumentParser

from handler_factory import handlers
from utils.path_transfer import to_eval_dir, to_handler_dir
from utils.lark_message import build_message, send_message

def result_catch(eval_dir):
    file_name = os.path.join(eval_dir, 'result.json')
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data['score']

def load_configs(config_path):
    with open(config_path, 'r') as f:
        configs = json.load(f)
    return configs

# def eval_finish(eval_dir, handler_name, mode):
#     if handler_name not in os.listdir(eval_dir):
#         return False, mode
#     if 'success.json' not in os.listdir(os.path.join(eval_dir, handler_name)):
#         return False, mode
#     try:
#         with open(os.path.join(eval_dir, handler_name, 'success.json'), 'r') as f:
#             success_dict = json.load(f)
#         if mode == 'infer+eval':
#             if success_dict['infer'] == 1 and success_dict['eval'] == 1:
#                 return True, mode
#             elif success_dict['infer'] == 1:
#                 return False, 'eval'
#             else:
#                 return False, mode
#         if mode == 'infer':
#             return success_dict['infer'] == 1, mode
#         if mode == 'eval':
#             # assert(success_dict['infer'] == 1)
#             return success_dict['eval'] == 1, mode
#     except:
#         return False, mode
    
#     return True, mode

def eval_finish(eval_dir, handler_name):
    if handler_name not in os.listdir(eval_dir):
        return False
    if 'result.json' not in os.listdir(os.path.join(eval_dir, handler_name)):
        return False
    return True


def load_result(eval_dir, handler):
    file_name = os.path.join(eval_dir, handler, 'result.json')
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data['score']

def get_ckpt_steps(ckpt_dir):
    return [s for s in os.listdir(ckpt_dir) if os.path.isdir(os.path.join(ckpt_dir, s)) and s != 'tensorboard' and not s.startswith('eval') and not s.startswith('tmp')]

def main_loop(config, exp_name, webhook_url, feishu_msg):
    logger.debug(f"config: {config}")
    ckpt_path = config['ckpt_path']

    step2result = defaultdict(dict)
    handler_configs = config['listen_config'][exp_name]

    ckpt_dir = os.path.join(ckpt_path, exp_name)
    if not os.path.exists(ckpt_dir):
        logger.warning(f'{ckpt_dir} has not been created')
        return False

    # 获取当前ckpt_dir下的所有step
    steps = get_ckpt_steps(ckpt_dir)
    extract_number = lambda s: int(re.search(r'\d+', s).group())
    steps = sorted(steps, key=extract_number)

    logger.debug(f"all step: {steps}")

    # 遍历每一个step
    for step in steps:
        update = False
        step_ckpt_path = os.path.join(ckpt_dir, step)

        eval_path = to_eval_dir(step_ckpt_path, exp_name)
        print(eval_path)
        logger.debug (f" handler config for this step: {eval_path}")

        # 遍历每个评测指标handler
        for handler, handler_config in handler_configs.items():
            cur_handler_config = handler_config.copy()
            # 判断当前step的评估handler进行状态
            finish_flag = eval_finish(eval_path, handler)
            # 如果已经完成则保存其评测结果
            if finish_flag:
                pre_handler_output_path = to_handler_dir(eval_path, handler)
                try:
                    r = result_catch(pre_handler_output_path)
                    step2result[step][handler] = r
                    logger.info(f"{handler} result exist, result: {r}", flush=True)
                    continue
                except Exception as e:
                    logger.exception(f"get score error, step: {step}, handler {handler}\ndetails: {e}")
                    logger.info(f"retrying handler {handler} in step {step}")
                
            logger.info(f"current step: {step}", flush=True)
            handler_output_path = to_handler_dir(eval_path, handler)
            cur_handler_config['model_path'] = step_ckpt_path
            cur_handler_config['output'] = handler_output_path 


            logger.debug(f" handler_config: {cur_handler_config}")
            logger.debug(f" handler_name: {handler}")
            logger.debug(f" handler_cmd: {handlers[handler]}")
            
            cmd = handlers[handler].format(**cur_handler_config)
            logger.debug(f"cmd: {cmd}")

            try:
                cmd_result = subprocess.run(cmd, shell=True)
                # mark_as_success(eval_path, handler)
            except Exception as e: 
                logger.exception(f"Error in cmd {cmd}. Error message: {e}")
                # if os.path.exists(handler_output_path):
                #     logger.debug(f'delete handler_output_path: {handler_output_path}')
                #     os.remove(handler_output_path)
                continue

            if cmd_result.returncode != 0:
                logger.error(f"Error in handler {handler}. Error message: {cmd_result.stderr}")
                continue
            try:
                score = result_catch(handler_output_path)
            except Exception as e:
                logger.exception(f"error: {e}")
                sys.exit(1)

            step2result[step][handler] = float(score)
            logger.info(f"SCORE: {score}")
            update = True
    
        if update:
            if feishu_msg:
                message = build_message(exp_name, step2result)
                send_message(webhook_url, message) 
            return True

    return False

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--config_path", type=str)
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--feishu_msg", type=int, default=1)

    args = parser.parse_args()
    config_path = args.config_path
    interval = args.interval
    feishu_msg = bool(args.feishu_msg)


    try:
        webhook_url = os.environ['WEBHOOK_URL']
    except Exception as e:
        logger.error(f'webhook_url has not been configured, exception: {e}')
        sys.exit(1)

    while True:
        try:
            watched_configs = load_configs(config_path)
            exec_flag = False
            for exp_name in watched_configs["ckpt_names"]:
                logger.debug(f"Checking for new ckpt in {exp_name}...")
                exec_flag = main_loop(watched_configs, exp_name, webhook_url, feishu_msg)
                if exec_flag:
                    break
            if not exec_flag:
                time.sleep(interval)
        except Exception as e:
            logger.exception(f"[INFO] error: {e}")
            message = f"帕鲁评测出错了: {e}"
            # send_message(webhook_url, message)
            sys.exit(1)