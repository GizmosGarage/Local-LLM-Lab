import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"


def normalize(text):
    return text.strip().lower().replace(",", "")


def evaluate(test):
    answer = test["answer"].strip()
    check = test["check"]
    expected = test["expected"]

    if check == "exact":
        return normalize(answer) == normalize(str(expected))

    if check == "contains":
        return normalize(str(expected)) in normalize(answer)

    if check == "bullet_count":
        lines = answer.splitlines()

        bullets = [
            line for line in lines
            if re.match(r"^\s*[-*•]\s+", line)
        ]

        return len(bullets) == expected

    if check == "sentence_count":
        sentences = [
            sentence for sentence in re.split(r"[.!?]+", answer)
            if sentence.strip()
        ]

        return len(sentences) == expected

    if check == "manual":
        return None

    return None


benchmark_files = sorted(RESULTS_DIR.glob("*-benchmark.json"))

for benchmark_file in benchmark_files:

    with open(benchmark_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    model = data["model"]

    automatic_correct = 0
    automatic_total = 0

    print(f"\n{model}")
    print("=" * len(model))

    for test in data["tests"]:
        passed = evaluate(test)

        if passed is None:
            status = "MANUAL REVIEW"
        else:
            automatic_total += 1

            if passed:
                automatic_correct += 1
                status = "PASS"
            else:
                status = "FAIL"

        print(
            f"{test['category']:22} "
            f"{test['test']:25} "
            f"{status}"
        )

    if automatic_total:
        percentage = automatic_correct / automatic_total * 100

        print(
            f"\nAutomatic score: "
            f"{automatic_correct}/{automatic_total} "
            f"({percentage:.1f}%)"
        )