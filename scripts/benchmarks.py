import json
import re
import time
from pathlib import Path

import requests


# file locations and server address

SERVER_URL = "http://127.0.0.1:8080"
CHAT_URL = f"{SERVER_URL}/v1/chat/completions"
MODELS_URL = f"{SERVER_URL}/v1/models"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_FILE = PROJECT_ROOT / "benchmarks" / "prompts.json"
RESULTS_DIR = PROJECT_ROOT / "results"


# load the benchmark prompts

with open(PROMPTS_FILE, "r", encoding="utf-8") as file:
    prompts = json.load(file)


# detect the running model

model_response = requests.get(MODELS_URL)
model_response.raise_for_status()

model_data = model_response.json()
model_name = model_data["data"][0]["id"]

print(f"Model detected: {model_name}")


# store the test results

results = []


# the benchmark loop

for test in prompts:
    print(f"\nRunning: {test['name']}")

    data = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": test["prompt"]
            }
        ],
        "temperature": 0,
        "seed": 42,
        "max_tokens": 200,
        "cache_prompt": False,
        "reasoning_effort": "none",
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }

    start_time = time.perf_counter()

    response = requests.post(
        CHAT_URL,
        json=data,
        timeout=300
    )

    end_time = time.perf_counter()

    response.raise_for_status()

    result = response.json()


# extract the useful results

    answer = result["choices"][0]["message"]["content"]

    usage = result.get("usage", {})
    timings = result.get("timings", {})

    benchmark_result = {
        "test": test["name"],
        "prompt": test["prompt"],
        "answer": answer,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "prompt_tokens_per_second": timings.get("prompt_per_second"),
        "generation_tokens_per_second": timings.get("predicted_per_second"),
        "total_request_seconds": round(end_time - start_time, 3)
    }

    results.append(benchmark_result)

    print(f"Prompt speed: {benchmark_result['prompt_tokens_per_second']} t/s")
    print(f"Generation speed: {benchmark_result['generation_tokens_per_second']} t/s")
    print(f"Total time: {benchmark_result['total_request_seconds']} s")


# save everything after the loop finishes

safe_model_name = re.sub(r"[^A-Za-z0-9._-]+", "_", model_name)

output_file = RESULTS_DIR / f"{safe_model_name}-benchmark.json"

output = {
    "model": model_name,
    "tests": results
}

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(output, file, indent=4)

print(f"\nBenchmark complete.")
print(f"Results saved to: {output_file}")