import json


def generate_summary_report(results: list, output_file: str = "report.json") -> dict:
    total_cases = len(results)
    avg_latency = (
        sum(r.latency_sec for r in results) / total_cases if total_cases else 0
    )

    # Categorize scores by evaluator name
    metric_breakdown = {}
    for r in results:
        for score in r.scores:
            if score.name not in metric_breakdown:
                metric_breakdown[score.name] = []
            metric_breakdown[score.name].append(score.score)

    # Compute averages per metric
    metric_averages = {
        metric_name: round(sum(scores) / len(scores), 3)
        for metric_name, scores in metric_breakdown.items()
    }

    summary = {
        "total_test_cases": total_cases,
        "avg_latency_sec": round(avg_latency, 3),
        "metric_scores": metric_averages,
        "all_passed": all(s.passed for r in results for s in r.scores),
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return summary
