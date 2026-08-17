from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur ILMR - Intelligent LLM Model Router"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


import time
import random

def small_model(query: str):
    """Simule un petit modèle : rapide et pas cher"""
    time.sleep(0.2)  # on simule un petit délai de traitement
    return {
        "response": f"[Small Model] Réponse simple à: '{query}'",
        "cost": 0.001,
        "latency": 0.2
    }

def large_model(query: str):
    """Simule un grand modèle : plus lent et plus cher"""
    time.sleep(1.0)  # on simule un délai plus long
    return {
        "response": f"[Large Model] Réponse détaillée et réfléchie à: '{query}'",
        "cost": 0.02,
        "latency": 1.0
    }

def analyze_request(query: str):
    """Analyse la requête et retourne ses caractéristiques"""
    word_count = len(query.split())
    return {
        "word_count": word_count
    }

def route_request(query: str):
    """Décide quel modèle utiliser selon la complexité de la requête"""
    features = analyze_request(query)

    if features["word_count"] < 10:
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

from fastapi import Query

@app.get("/route")
def route(query: str = Query(...)):
    return route_request(query)