from analyzer import analyze_request
from model_registry import get_model_info, list_available_models


# --- Ancienne approche (Baseline 2 : règles) ---
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


# --- Nouvelle approche (Stratégie score pondéré, section 10) ---
WEIGHTS = {
    "alpha": 1.0,   # poids de la qualité
    "beta": 3.0,    # poids du coût (pénalité)
    "gamma": 1.0,   # poids de la latence (pénalité)
}


def compute_score(model_info: dict) -> float:
    """Calcule le score d'un modèle selon la formule pondérée"""
    quality = model_info["quality_score"]
    cost = model_info["cost_per_call"]
    latency = model_info["avg_latency"]

    score = (
        WEIGHTS["alpha"] * quality
        - WEIGHTS["beta"] * cost
        - WEIGHTS["gamma"] * latency
    )
    return score


def required_quality(features: dict) -> float:
    """Détermine le niveau de qualité minimum requis, selon la complexité de la requête"""
    if features["has_code"] or features["has_reasoning_keywords"]:
        return 0.85
    if features["word_count"] > 25:
        return 0.85
    if features["word_count"] > 10:
        return 0.7
    return 0.0


def decide_model_by_score(features: dict) -> str:
    """Choisit le modèle avec le meilleur score, parmi les modèles qui atteignent
    le niveau de qualité minimum requis par la requête"""
    min_quality = required_quality(features)

    best_model_name = None
    best_score = float("-inf")

    for model_name in list_available_models():
        model_info = get_model_info(model_name)

        if model_info["quality_score"] < min_quality:
            continue

        score = compute_score(model_info)

        if score > best_score:
            best_score = score
            best_model_name = model_name

    return best_model_name


# --- Fonction principale, utilisée par l'API ---
def route_request(query: str, strategy: str = "score"):
    """Analyse la requête, choisit un modèle, et l'exécute"""
    features = analyze_request(query)

    if strategy == "rules":
        chosen_model_name = decide_model(features)
    else:
        chosen_model_name = decide_model_by_score(features)

    model_info = get_model_info(chosen_model_name)
    model_function = model_info["function"]
    result = model_function(query)

    return {
        "strategy_used": strategy,
        "chosen_model": chosen_model_name,
        "model_metadata": {
            "expected_cost": model_info["cost_per_call"],
            "expected_latency": model_info["avg_latency"],
            "expected_quality": model_info["quality_score"]
        },
        "features": features,
        "result": result
    }