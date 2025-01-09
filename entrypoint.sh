#!/bin/bash


export VLLM_ALLOW_RUNTIME_LORA_UPDATING=True
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Start OpenResty in the background and start vllm server
/usr/local/openresty/bin/openresty -g 'daemon on;' && python3 -m vllm.entrypoints.openai.api_server --model meta-llama/Llama-3.1-70B-Instruct --tensor-parallel-size 4 --dtype=bfloat16 --max_model_len=4096 --enable-lora



