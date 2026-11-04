from router import route_with_cascade


def test_cascade_cost_counts_every_attempt():
    """Régression : le coût d'un cascade doit inclure TOUS les modèles essayés,
    pas seulement le dernier."""
    query = "Analyse en detail ce systeme distribue complexe et explique precisement ses avantages et inconvenients"
    outcome = route_with_cascade(query)

    assert outcome["total_cost"] >= outcome["result"]["cost"]
    if outcome["escalated"]:
        assert outcome["total_cost"] > outcome["result"]["cost"]
        assert outcome["total_latency"] > outcome["result"]["latency"]