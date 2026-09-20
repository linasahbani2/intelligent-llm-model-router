import time
import random


def estimate_confidence(query: str, model_size: str) -> float:
    """Simule un score de confiance (0 à 1) selon la complexité de la requête
    et la puissance du modèle qui répond"""
    word_count = len(query.split())

    base_confidence = {
        "small": 0.9,
        "medium": 0.85,
        "large": 0.95,
    }[model_size]

    complexity_penalty = {
        "small": 0.04,
        "medium": 0.015,
        "large": 0.003,
    }[model_size]

    confidence = base_confidence - (word_count * complexity_penalty)
    confidence += random.uniform(-0.05, 0.05)
    confidence = max(0.0, min(1.0, confidence))

    return round(confidence, 3)


def small_model(query: str):
    """Simule un petit modèle : rapide et pas cher"""
    time.sleep(0.2)
    return {
        "response": f"[Small Model] Réponse simple à: '{query}'",
        "cost": 0.001,
        "latency": 0.2,
        "confidence": estimate_confidence(query, "small"),
    }


def medium_model(query: str):
    """Simule un modèle moyen : équilibre entre vitesse et qualité"""
    time.sleep(0.5)
    return {
        "response": f"[Medium Model] Réponse équilibrée à: '{query}'",
        "cost": 0.008,
        "latency": 0.5,
        "confidence": estimate_confidence(query, "medium"),
    }


def large_model(query: str):
    """Simule un grand modèle : plus lent et plus cher"""
    time.sleep(1.0)
    return {
        "response": f"[Large Model] Réponse détaillée et réfléchie à: '{query}'",
        "cost": 0.02,
        "latency": 1.0,
        "confidence": estimate_confidence(query, "large"),
    }