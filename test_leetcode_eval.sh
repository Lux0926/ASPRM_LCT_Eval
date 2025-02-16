python src/main_eval.py  --model_name "model" \
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
                --input_file "result_s2prm_datacodeandmathmistralv3_modelds_bz64_lr4e6_epo1_no_con_confidence_leetCoTE_64_ds_data.jsonl" \
                --output_file "result_s2prm_datacodeandmathmistralv3_modelds_bz64_lr4e6_epo1_no_con_confidence_leetCoTE_64_ds_data.jsonl" &
