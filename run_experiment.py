import json
import random
from sklearn.model_selection import train_test_split
from router import route_request

STRATEGIES = ["always_large", "rules", "score", "cascade", "ml"]
SAMPLE_SIZE = 150


def load_eval_queries():
    """Reconstruit exactement le même split entraînement/test que train_classifier.py,
    et pioche l'échantillon d'évaluation UNIQUEMENT dans le test set,
    pour ne jamais évaluer le classifieur ML sur des données qu'il a vues à l'entraînement."""
    with open("labeled_dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data]
    labels = [item["label"] for item in data]

    _, X_test, _, _ = train_test_split(
        texts, labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )

    random.seed(42)
    sample = random.sample(X_test, SAMPLE_SIZE)
    return sample


def run_comparison(queries):
    results = {}

    for strategy in STRATEGIES:
        total_cost = 0.0
        total_latency = 0.0
        total_quality = 0.0
        model_counts = {"small": 0, "medium": 0, "large": 0}

        for query in queries:
            response = route_request(query, strategy)
            metadata = response["model_metadata"]

            total_cost += metadata["expected_cost"]
            total_latency += metadata["expected_latency"]
            total_quality += metadata["expected_quality"]
            model_counts[response["chosen_model"]] += 1

        n = len(queries)
        results[strategy] = {
            "avg_cost": total_cost / n,
            "avg_latency": total_latency / n,
            "avg_quality": total_quality / n,
            "model_distribution": model_counts,
        }

    return results


def print_report(results: dict, n_queries: int):
    print(f"\nÉvaluation sur {n_queries} requêtes réelles (issues du test set Dolly-15k, jamais vues à l'entraînement)\n")
    print(f"{'Stratégie':<15} {'Coût moy.':<12} {'Latence moy.':<15} {'Qualité moy.':<15} {'Distribution'}")
    print("-" * 90)
    for strategy, stats in results.items():
        dist = stats["model_distribution"]
        dist_str = f"S:{dist['small']} M:{dist['medium']} L:{dist['large']}"
        print(f"{strategy:<15} {stats['avg_cost']:<12.4f} {stats['avg_latency']:<15.3f} {stats['avg_quality']:<15.3f} {dist_str}")


if __name__ == "__main__":
    queries = load_eval_queries()
    results = run_comparison(queries)
    print_report(results, len(queries))