import time

from fastapi import FastAPI, Query, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from router import route_request

app = FastAPI()

KNOWN_STRATEGIES = {"always_large", "rules", "score", "cascade", "ml"}

REQUESTS = Counter(
    "ilmr_requests_total",
    "Nombre de requêtes routées, par stratégie et par modèle final",
    ["strategy", "chosen_model"],
)
COST = Counter(
    "ilmr_cost_total",
    "Coût simulé cumulé, par stratégie",
    ["strategy"],
)
ESCALATIONS = Counter(
    "ilmr_cascade_escalations_total",
    "Nombre de requêtes du cascade qui ont dû escalader vers un modèle plus gros",
)
DURATION = Histogram(
    "ilmr_request_duration_seconds",
    "Durée réelle de traitement d'une requête, par stratégie",
    ["strategy"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0),
)


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur ILMR - Intelligent LLM Model Router"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    """Expose les métriques au format texte que Prometheus sait lire"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/route")
def route(query: str = Query(...), strategy: str = Query("score")):
    # Une stratégie inconnue est traitée comme "score" par le router : on utilise le même
    # nom pour les métriques, pour qu'un client ne puisse pas créer des séries à l'infini.
    strategy_label = strategy if strategy in KNOWN_STRATEGIES else "score"

    start = time.perf_counter()
    response = route_request(query, strategy)
    duration = time.perf_counter() - start

    REQUESTS.labels(strategy=strategy_label, chosen_model=response["chosen_model"]).inc()
    COST.labels(strategy=strategy_label).inc(response["model_metadata"]["expected_cost"])
    DURATION.labels(strategy=strategy_label).observe(duration)
    if response.get("escalated"):
        ESCALATIONS.inc()

    return response