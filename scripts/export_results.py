import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

OUTPUT_FILE = RESULTS_DIR / "benchmark-summary.csv"
MODELS_FILE = PROJECT_ROOT / "benchmarks" / "models.json"

benchmark_files = sorted(RESULTS_DIR.glob("*-benchmark.json"))

with open(MODELS_FILE, "r", encoding="utf-8") as file:
    models = json.load(file)


rows = []

for benchmark_file in benchmark_files:
    with open(benchmark_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    model = data["model"]
    metadata = models[model]

    for test in data["tests"]:
        rows.append(
            {
                "model": model,
                "parameters": metadata["parameters"],
                "quantization": metadata["quantization"],
                "context": metadata["context"],
                "gpu": metadata["gpu"],
                "gpu_layers": metadata["gpu_layers"],
                "model_vram_mib": metadata["model_vram_mib"],
                "test": test["test"],
                "category": test["category"],
                "prompt_tokens": test["prompt_tokens"],
                "completion_tokens": test["completion_tokens"],
                "total_tokens": test["total_tokens"],
                "prompt_tokens_per_second": test["prompt_tokens_per_second"],
                "generation_tokens_per_second": test["generation_tokens_per_second"],
                "total_request_seconds": test["total_request_seconds"],
            }
        )


fieldnames = [
    "model",
    "parameters",
    "quantization",
    "context",
    "gpu",
    "gpu_layers",
    "model_vram_mib",
    "test",
    "category",
    "prompt_tokens",
    "completion_tokens",
    "total_tokens",
    "prompt_tokens_per_second",
    "generation_tokens_per_second",
    "total_request_seconds",
]


with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(rows)


print(f"Exported {len(rows)} benchmark results.")
print(f"Saved to: {OUTPUT_FILE}")