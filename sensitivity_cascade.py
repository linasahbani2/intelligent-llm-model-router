import os
os.environ.setdefault("SIMULATE_DELAY", "0")  # pas d'attente simulée pendant les expériences

import random
import models
from router import route_request
from run_experiment import load_eval_queries

PENALTY_SCALES = [1.0, 0.5, 0.25, 0.1, 0.05]
BASELINE_COST = 0.0200      # always_large
BASELINE_LATENCY = 1.000    # always_large


def run_cascade(queries):
    total_cost = 0.0
    total_latency = 0.0
    total_quality = 0.0
    total_attempts = 0
    final_model_counts = {"small": 0, "medium": 0, "large": 0}

    for query in queries:
        response = route_request(query, "cascade")
        metadata = response["model_metadata"]

        total_cost += metadata["expected_cost"]
        total_latency += metadata["expected_latency"]
        total_quality += metadata["expected_quality"]
        total_attempts += len(response["attempted_models"])
        final_model_counts[response["chosen_model"]] += 1

    n = len(queries)
    return {
        "avg_cost": total_cost / n,
        "avg_latency": total_latency / n,
        "avg_quality": total_quality / n,
        "avg_attempts": total_attempts / n,
        "final_models": final_model_counts,
    }


def main():
    queries = load_eval_queries()
    n = len(queries)

    print(f"\nSensibilité du Cascade à la pénalité de confiance ({n} requêtes, seuil de confiance = 0.75)")
    print(f"Baseline always_large : coût={BASELINE_COST:.4f} | latence={BASELINE_LATENCY:.3f} | qualité=0.950\n")
    header = (f"{'Échelle':<9}{'Pén./mot(small)':<17}{'Coût moy.':<11}{'vs base':<10}"
              f"{'Latence':<9}{'Qualité':<9}{'Essais/req':<12}{'Modèle final'}")
    print(header)
    print("-" * 95)

    for scale in PENALTY_SCALES:
        models.PENALTY_SCALE = scale
        random.seed(42)  # même graine pour chaque échelle : comparaison équitable
        stats = run_cascade(queries)

        vs_base = (stats["avg_cost"] / BASELINE_COST - 1) * 100
        final = stats["final_models"]
        final_str = f"S:{final['small']} M:{final['medium']} L:{final['large']}"
        print(f"{scale:<9}{0.04 * scale:<17.4f}{stats['avg_cost']:<11.4f}{vs_base:+8.1f}% "
              f"{stats['avg_latency']:<9.3f}{stats['avg_quality']:<9.3f}{stats['avg_attempts']:<12.2f}{final_str}")

    models.PENALTY_SCALE = 1.0  # on remet la valeur d'origine


if __name__ == "__main__":
    main()