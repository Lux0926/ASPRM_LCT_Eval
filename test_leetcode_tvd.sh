python src/main_tvd.py  --model_name "model" \
                --task "LeetCodeTest" \
                --save "sft_old_test" \
                --num_gpus 4 \
                --num_samples 1 \
                --k 1 \
                --temperature 0.0 \
                --num_workers 32 \
                --batch_size 200 \
                --max_tokens 8192 \
                --model_type "Chat" \
                --prompt_type "Instruction" \
                --prompt_prefix "" \
                --prompt_suffix "" \
                --trust_remote_code \
                --input_file "s2prm_datacodeandmathmistralv3_modelds_bz64_lr5e6_epo1_no_con_con22_lct.jsonl" \
                --output_file "s2prm_datads_modelds_bz32_lr5e6_epo1_no_con_con30.jsonl"
