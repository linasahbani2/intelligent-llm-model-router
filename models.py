import time

def small_model(query: str):
    """Simule un petit modèle : rapide et pas cher"""
    time.sleep(0.2)
    return {
        "response": f"[Small Model] Réponse simple à: '{query}'",
        "cost": 0.001,
        "latency": 0.2
    }

def large_model(query: str):
    """Simule un grand modèle : plus lent et plus cher"""
    time.sleep(1.0)
    return {
        "response": f"[Large Model] Réponse détaillée et réfléchie à: '{query}'",
        "cost": 0.02,
        "latency": 1.0
    }

def medium_model(query: str):
    """Simule un modèle moyen : équilibre entre vitesse et qualité"""
    time.sleep(0.5)
    return {
        "response": f"[Medium Model] Réponse équilibrée à: '{query}'",
        "cost": 0.008,
        "latency": 0.5
    }