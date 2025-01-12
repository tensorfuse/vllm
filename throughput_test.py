import json
import time
import asyncio
import aiohttp
from typing import Dict

# Function to send a request
async def send_request(session: aiohttp.ClientSession, prompt: str) -> Dict:
    url = "http://a5ca9a76fc0dc4f33acaa5196bba6ca5-1703175632.us-east-1.elb.amazonaws.com/svc/default/docker-test-gpus-4-l40s/v1/chat/completions"
    payload = {
        "model": "gane5hvarma/joe-adapter",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    async with session.post(url, json=payload, headers=headers) as response:
        # Force parse as JSON regardless of Content-Type
        text = await response.text()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            print(f"Error: Could not parse response as JSON. Content: {text}")
            raise

# Function to measure throughput
async def measure_throughput(
    num_concurrent_requests: int = 100,
    prompt: str = "hello"
) -> float:
    async with aiohttp.ClientSession() as session:
        start_time = time.time()

        # Create tasks for all requests
        tasks = [send_request(session, prompt) for _ in range(num_concurrent_requests)]

        # Wait for all requests to complete
        results = await asyncio.gather(*tasks)

        end_time = time.time()
        total_time = end_time - start_time

        # Calculate total tokens processed
        total_tokens = sum(
            result["usage"]["total_tokens"] for result in results if "usage" in result
        )

        throughput = total_tokens / total_time if total_time > 0 else 0
        return throughput, total_time, len(results)

# Main function to test throughput for different concurrent loads
async def main():
    concurrent_requests = [10, 50, 100, 200, 500, 1000]
    print("Measuring vLLM throughput with different concurrent request loads...")
    print("\nRequests | Throughput (tokens/sec) | Total Time (s)")
    print("-" * 50)

    for num_requests in concurrent_requests:
        try:
            throughput, total_time, completed = await measure_throughput(num_requests)
            print(f"{num_requests:8d} | {throughput:19.2f} | {total_time:13.2f}")
        except Exception as e:
            print(f"Error during test with {num_requests} requests: {e}")

if __name__ == "__main__":
    asyncio.run(main())