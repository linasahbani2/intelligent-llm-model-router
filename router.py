from analyzer import analyze_request
from model_registry import get_model_info


def decide_model(features: dict) -> str:
    """Décide quel modèle utiliser selon les caractéristiques de la requête"""
    if features["has_code"] or features["has_reasoning_keywords"]:
        if features["word_count"] > 20:
            return "large"
        else:
            return "medium"

    if features["word_count"] < 10:
        return "small"
    elif features["word_count"] < 25:
        return "medium"
    else:
        return "large"


def route_request(query: str):
    """Analyse la requête, choisit un modèle via le Registry, et l'exécute"""
    features = analyze_request(query)
    chosen_model_name = decide_model(features)

    model_info = get_model_info(chosen_model_name)
    model_function = model_info["function"]
    result = model_function(query)

    return {
        "chosen_model": chosen_model_name,
        "model_metadata": {
            "expected_cost": model_info["cost_per_call"],
            "expected_latency": model_info["avg_latency"],
            "expected_quality": model_info["quality_score"]
        },
        "features": features,
        "result": result
    }