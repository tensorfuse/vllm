import json
import time
import asyncio
import aiohttp
import numpy as np
from typing import Dict, List

async def send_request(session: aiohttp.ClientSession, prompt: str, max_tokens: int = 100) -> Dict:
    url = "http://a3bafe67e8f2a422ba99b5737992f756-614062644.us-east-1.elb.amazonaws.com/svc/default/vllm-gpus-1-a10g/v1/completions"
    payload = {
        "model": "google/gemma-2b",
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    async with session.post(url, json=payload) as response:
        return await response.json()

async def measure_throughput(
    num_concurrent_requests: int = 100,
    prompt: str = "Tell me a story about Tensorfuse",
    max_tokens: int = 1000
) -> float:
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        
        # Create tasks for all requests
        tasks = [
            send_request(session, prompt, max_tokens)
            for _ in range(num_concurrent_requests)
        ]
        
        # Wait for all requests to complete
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calculate total tokens processed
        total_tokens = sum(
            result["usage"]["completion_tokens"]
            for result in results
        )
        
        throughput = total_tokens / total_time
        return throughput, total_time, len(results)

async def main():
    concurrent_requests = [10, 50, 100, 200,500,1000]
    print("Measuring vLLM throughput with different concurrent request loads...")
    print("\nRequests | Throughput (tokens/sec) | Total Time (s)")
    print("-" * 50)
    
    for num_requests in concurrent_requests:
        throughput, total_time, completed = await measure_throughput(num_requests)
        print(f"{num_requests:8d} | {throughput:19.2f} | {total_time:13.2f}")

if __name__ == "__main__":
    asyncio.run(main())

