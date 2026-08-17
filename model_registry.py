from models import small_model, medium_model, large_model

MODEL_REGISTRY = {
    "small": {
        "function": small_model,
        "size": "small",
        "cost_per_call": 0.001,
        "avg_latency": 0.2,
        "quality_score": 0.6
    },
    "medium": {
        "function": medium_model,
        "size": "medium",
        "cost_per_call": 0.008,
        "avg_latency": 0.5,
        "quality_score": 0.8
    },
    "large": {
        "function": large_model,
        "size": "large",
        "cost_per_call": 0.02,
        "avg_latency": 1.0,
        "quality_score": 0.95
    }
}


def get_model_info(model_name: str):
    """Retourne les infos d'un modèle par son nom"""
    return MODEL_REGISTRY.get(model_name)


def list_available_models():
    """Retourne la liste des noms de modèles disponibles"""
    return list(MODEL_REGISTRY.keys())