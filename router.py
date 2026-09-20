from analyzer import analyze_request
from model_registry import get_model_info, list_available_models
from models import small_model, medium_model, large_model


# --- Baseline 1 : toujours le plus grand modèle ---
def decide_model_always_large(features: dict) -> str:
    """Baseline 1 : utilise toujours le modèle le plus puissant"""
    return "large"


# --- Baseline 2 : règles ---
def decide_model(features: dict) -> str:
    """Décide quel modèle utiliser selon les caractéristiques de la requête"""
    if features["has_code"] or features["has_reasoning_keywords"]:
        if features["word_count"] > 15:
            return "large"
        else:
            return "medium"

    if features["word_count"] < 10:
        return "small"
    elif features["word_count"] < 25:
        return "medium"
    else:
        return "large"


# --- Stratégie score pondéré (section 10) ---
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


# --- Stratégie Cascade (section 12) ---
CONFIDENCE_THRESHOLD = 0.75

CASCADE_ORDER = [
    ("small", small_model),
    ("medium", medium_model),
    ("large", large_model),
]


def route_with_cascade(query: str):
    """Essaie le modèle le moins cher en premier,
    escalade vers un modèle plus puissant seulement si la confiance est trop basse"""
    for model_name, model_function in CASCADE_ORDER:
        result = model_function(query)

        if result["confidence"] >= CONFIDENCE_THRESHOLD:
            return {
                "chosen_model": model_name,
                "escalated": model_name != "small",
                "result": result,
            }

    # Si on arrive ici, même "large" n'était pas confiant : on renvoie sa réponse quand même
    return {
        "chosen_model": "large",
        "escalated": True,
        "result": result,
    }


# --- Fonction principale, utilisée par l'API ---
def route_request(query: str, strategy: str = "score"):
    """Analyse la requête, choisit un modèle, et l'exécute"""
    features = analyze_request(query)

    if strategy == "rules":
        chosen_model_name = decide_model(features)
    elif strategy == "always_large":
        chosen_model_name = decide_model_always_large(features)
    elif strategy == "cascade":
        cascade_result = route_with_cascade(query)
        model_info = get_model_info(cascade_result["chosen_model"])
        return {
            "strategy_used": strategy,
            "chosen_model": cascade_result["chosen_model"],
            "escalated": cascade_result["escalated"],
            "model_metadata": {
                "expected_cost": model_info["cost_per_call"],
                "expected_latency": model_info["avg_latency"],
                "expected_quality": model_info["quality_score"]
            },
            "features": features,
            "result": cascade_result["result"],
        }
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