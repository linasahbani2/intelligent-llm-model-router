from analyzer import analyze_request
from models import small_model, large_model

def route_request(query: str):
    """Décide quel modèle utiliser selon la complexité de la requête"""
    features = analyze_request(query)

    is_simple = (
        features["word_count"] < 10
        and not features["has_code"]
        and not features["has_reasoning_keywords"]
    )

    if is_simple:
        chosen_model = "small"
        result = small_model(query)
    else:
        chosen_model = "large"
        result = large_model(query)

    return {
        "chosen_model": chosen_model,
        "features": features,
        "result": result
    }