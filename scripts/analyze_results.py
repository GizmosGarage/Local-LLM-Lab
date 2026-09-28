import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"
INPUT_FILE = RESULTS_DIR / "benchmark-summary.csv"
OUTPUT_FILE = RESULTS_DIR / "model-summary.csv"
CHARTS_DIR = RESULTS_DIR / "charts"


model_data = defaultdict(
    lambda: {
        "prompt_speeds": [],
        "generation_speeds": [],
        "request_times": [],
    }
)


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        model = row["model"]

        model_data[model]["prompt_speeds"].append(
            float(row["prompt_tokens_per_second"])
        )

        model_data[model]["generation_speeds"].append(
            float(row["generation_tokens_per_second"])
        )

        model_data[model]["request_times"].append(
            float(row["total_request_seconds"])
        )


summary_rows = []

for model, data in model_data.items():
    average_prompt_speed = (
        sum(data["prompt_speeds"]) / len(data["prompt_speeds"])
    )

    average_generation_speed = (
        sum(data["generation_speeds"])
        / len(data["generation_speeds"])
    )

    average_request_time = (
        sum(data["request_times"])
        / len(data["request_times"])
    )

    summary_rows.append(
        {
            "model": model,
            "average_prompt_tokens_per_second": round(
                average_prompt_speed, 2
            ),
            "average_generation_tokens_per_second": round(
                average_generation_speed, 2
            ),
            "average_request_seconds": round(
                average_request_time, 2
            ),
        }
    )


with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    fieldnames = [
        "model",
        "average_prompt_tokens_per_second",
        "average_generation_tokens_per_second",
        "average_request_seconds",
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(summary_rows)


print("\nModel averages")
print("==============")

for row in summary_rows:
    print(f"\n{row['model']}")
    print(
        "Prompt speed:     "
        f"{row['average_prompt_tokens_per_second']} t/s"
    )
    print(
        "Generation speed: "
        f"{row['average_generation_tokens_per_second']} t/s"
    )
    print(
        "Request time:     "
        f"{row['average_request_seconds']} s"
    )


models = [row["model"] for row in summary_rows]

generation_speeds = [
    row["average_generation_tokens_per_second"]
    for row in summary_rows
]

request_times = [
    row["average_request_seconds"]
    for row in summary_rows
]


plt.figure()

plt.bar(models, generation_speeds)

plt.title("Average LLM Generation Speed")
plt.xlabel("Model")
plt.ylabel("Tokens per second")

plt.tight_layout()

generation_chart = CHARTS_DIR / "generation-speed.png"

plt.savefig(generation_chart)
plt.close()


plt.figure()

plt.bar(models, request_times)

plt.title("Average LLM Request Time")
plt.xlabel("Model")
plt.ylabel("Seconds")

plt.tight_layout()

request_chart = CHARTS_DIR / "request-time.png"

plt.savefig(request_chart)
plt.close()


print(f"\nSummary saved to: {OUTPUT_FILE}")
print(f"Generation chart saved to: {generation_chart}")
print(f"Request-time chart saved to: {request_chart}")