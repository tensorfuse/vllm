#!/bin/bash


export VLLM_ALLOW_RUNTIME_LORA_UPDATING=True
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Start OpenResty in the background and start vllm server
/usr/local/openresty/bin/openresty -g 'daemon on;' && python3 -m vllm.entrypoints.openai.api_server --model deepseek-ai/DeepSeek-V3 --tensor-parallel-size 4 --dtype=bfloat16 --max_model_len=4096
