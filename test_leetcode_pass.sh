python src/main_pass.py  --model_name "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/dataset_process/deepseek-coder-6.7b-instruct_sft_biao_bz64_5e6_tem_1115/model" \
                --task "LeetCodeTest" \
                --save "sft_old_test" \
                --num_gpus 4 \
                --num_samples 1 \
                --k 1 \
                --pass_size 1 \
                --temperature 0.0 \
                --num_workers 32 \
                --batch_size 200 \
                --max_tokens 8192 \
                --model_type "Chat" \
                --prompt_type "Instruction" \
                --prompt_prefix "" \
                --prompt_suffix "" \
                --trust_remote_code \
                --input_file "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/eval/leetcode_eval_dataset_solution_merge_bo256_hardrandom.jsonl" \
                --output_file "pass1.jsonl" &


python src/main_pass.py  --model_name "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/dataset_process/deepseek-coder-6.7b-instruct_sft_biao_bz64_5e6_tem_1115/model" \
                --task "LeetCodeTest" \
                --save "sft_old_test" \
                --num_gpus 4 \
                --num_samples 1 \
                --k 1 \
                --pass_size 4 \
                --temperature 0.0 \
                --num_workers 32 \
                --batch_size 200 \
                --max_tokens 8192 \
                --model_type "Chat" \
                --prompt_type "Instruction" \
                --prompt_prefix "" \
                --prompt_suffix "" \
                --trust_remote_code \
                --input_file "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/eval/leetcode_eval_dataset_solution_merge_bo256_hardrandom.jsonl" \
                --output_file "pass4.jsonl" &

python src/main_pass.py  --model_name "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/dataset_process/deepseek-coder-6.7b-instruct_sft_biao_bz64_5e6_tem_1115/model" \
                --task "LeetCodeTest" \
                --save "sft_old_test" \
                --num_gpus 4 \
                --num_samples 1 \
                --k 1 \
                --pass_size 8 \
                --temperature 0.0 \
                --num_workers 32 \
                --batch_size 200 \
                --max_tokens 8192 \
                --model_type "Chat" \
                --prompt_type "Instruction" \
                --prompt_prefix "" \
                --prompt_suffix "" \
                --trust_remote_code \
                --input_file "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/eval/leetcode_eval_dataset_solution_merge_bo256_hardrandom.jsonl" \
                --output_file "pass8.jsonl" &

python src/main_pass.py  --model_name "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/dataset_process/deepseek-coder-6.7b-instruct_sft_biao_bz64_5e6_tem_1115/model" \
                --task "LeetCodeTest" \
                --save "sft_old_test" \
                --num_gpus 4 \
                --num_samples 1 \
                --k 1 \
                --pass_size 16 \
                --temperature 0.0 \
                --num_workers 32 \
                --batch_size 200 \
                --max_tokens 8192 \
                --model_type "Chat" \
                --prompt_type "Instruction" \
                --prompt_prefix "" \
                --prompt_suffix "" \
                --trust_remote_code \
                --input_file "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/eval/leetcode_eval_dataset_solution_merge_bo256_hardrandom.jsonl" \
                --output_file "pass16.jsonl" &


python src/main_pass.py  --model_name "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/dataset_process/deepseek-coder-6.7b-instruct_sft_biao_bz64_5e6_tem_1115/model" \
                --task "LeetCodeTest" \
                --save "sft_old_test" \
                --num_gpus 4 \
                --num_samples 1 \
                --k 1 \
                --pass_size 32 \
                --temperature 0.0 \
                --num_workers 32 \
                --batch_size 200 \
                --max_tokens 8192 \
                --model_type "Chat" \
                --prompt_type "Instruction" \
                --prompt_prefix "" \
                --prompt_suffix "" \
                --trust_remote_code \
                --input_file "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/eval/leetcode_eval_dataset_solution_merge_bo256_hardrandom.jsonl" \
                --output_file "pass32.jsonl" &

python src/main_pass.py  --model_name "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/dataset_process/deepseek-coder-6.7b-instruct_sft_biao_bz64_5e6_tem_1115/model" \
                --task "LeetCodeTest" \
                --save "sft_old_test" \
                --num_gpus 4 \
                --num_samples 1 \
                --k 1 \
                --pass_size 64 \
                --temperature 0.0 \
                --num_workers 32 \
                --batch_size 200 \
                --max_tokens 8192 \
                --model_type "Chat" \
                --prompt_type "Instruction" \
                --prompt_prefix "" \
                --prompt_suffix "" \
                --trust_remote_code \
                --input_file "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/eval/leetcode_eval_dataset_solution_merge_bo256_hardrandom.jsonl" \
                --output_file "pass64.jsonl" &



