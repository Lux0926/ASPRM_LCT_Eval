cd /inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/oce_new_v2

python src/main.py  --model_name "/inspire/hdd/ws-f4d69b29-e0a5-44e6-bd92-acf4de9990f0/public-project/liuyuliang-240108350135/S2PRM/lux_newcode/code/new_model1211/ds_code_bz32_lr1e5_epo1" \
                --task "LeetCodeTest" \
                --save "sft_old_test_1213" \
                --num_gpus 1 \
                --num_samples 1 \
                --k 1 \
                --temperature 0.0 \
                --num_workers 10 \
                --batch_size 200 \
                --max_tokens 4096 \
                --prompt_prefix "" \
                --prompt_suffix "" \
                --trust_remote_code \
                --model_type "Chat" \
                --prompt_type "Instruction" \