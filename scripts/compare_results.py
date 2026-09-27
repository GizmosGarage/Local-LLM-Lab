import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

benchmark_files = list(RESULTS_DIR.glob("*-benchmark.json"))

for benchmark_file in benchmark_files:
    with open(benchmark_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    model = data["model"]
    tests = data["tests"]

    prompt_speeds = [
        test["prompt_tokens_per_second"]
        for test in tests
        if test["prompt_tokens_per_second"] is not None
    ]

    generation_speeds = [
        test["generation_tokens_per_second"]
        for test in tests
        if test["generation_tokens_per_second"] is not None
    ]

    request_times = [
        test["total_request_seconds"]
        for test in tests
    ]

    average_prompt_speed = sum(prompt_speeds) / len(prompt_speeds)
    average_generation_speed = sum(generation_speeds) / len(generation_speeds)
    average_request_time = sum(request_times) / len(request_times)

    print(f"\n{model}")
    print("-" * len(model))
    print(f"Average prompt speed:     {average_prompt_speed:.2f} t/s")
    print(f"Average generation speed: {average_generation_speed:.2f} t/s")
    print(f"Average request time:     {average_request_time:.2f} s")