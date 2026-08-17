from dataset import TEST_QUERIES
from router import route_request

STRATEGIES = ["always_large", "rules", "score"]


def run_comparison():
    results = {}

    for strategy in STRATEGIES:
        total_cost = 0.0
        total_latency = 0.0
        total_quality = 0.0
        model_counts = {"small": 0, "medium": 0, "large": 0}

        for query in TEST_QUERIES:
            response = route_request(query, strategy)
            metadata = response["model_metadata"]

            total_cost += metadata["expected_cost"]
            total_latency += metadata["expected_latency"]
            total_quality += metadata["expected_quality"]
            model_counts[response["chosen_model"]] += 1

        n = len(TEST_QUERIES)
        results[strategy] = {
            "avg_cost": total_cost / n,
            "avg_latency": total_latency / n,
            "avg_quality": total_quality / n,
            "model_distribution": model_counts,
        }

    return results


def print_report(results: dict):
    print(f"\n{'Stratégie':<15} {'Coût moy.':<12} {'Latence moy.':<15} {'Qualité moy.':<15} {'Distribution'}")
    print("-" * 90)
    for strategy, stats in results.items():
        dist = stats["model_distribution"]
        dist_str = f"S:{dist['small']} M:{dist['medium']} L:{dist['large']}"
        print(f"{strategy:<15} {stats['avg_cost']:<12.4f} {stats['avg_latency']:<15.3f} {stats['avg_quality']:<15.3f} {dist_str}")


if __name__ == "__main__":
    results = run_comparison()
    print_report(results)