from router import (
    decide_model,
    decide_model_by_score,
    compute_score,
    required_quality,
)
from model_registry import get_model_info


def test_decide_model_simple_query_returns_small():
    features = {"word_count": 3, "has_code": False, "has_reasoning_keywords": False}
    assert decide_model(features) == "small"


def test_decide_model_code_query_returns_medium_or_large():
    features = {"word_count": 5, "has_code": True, "has_reasoning_keywords": False}
    assert decide_model(features) == "medium"


def test_required_quality_is_high_for_reasoning_queries():
    features = {"word_count": 5, "has_code": False, "has_reasoning_keywords": True}
    assert required_quality(features) == 0.85


def test_required_quality_is_zero_for_simple_queries():
    features = {"word_count": 3, "has_code": False, "has_reasoning_keywords": False}
    assert required_quality(features) == 0.0


def test_score_strategy_picks_cheapest_for_simple_query():
    """Test de régression : une requête simple doit choisir le modèle le moins cher"""
    features = {"word_count": 3, "has_code": False, "has_reasoning_keywords": False}
    assert decide_model_by_score(features) == "small"


def test_score_strategy_respects_quality_threshold_for_complex_query():
    """Test de régression : LE bug qu'on a corrigé.
    Une requête complexe doit choisir un modèle assez bon, jamais le moins cher
    juste parce qu'il a le meilleur score brut."""
    features = {"word_count": 20, "has_code": False, "has_reasoning_keywords": True}
    chosen = decide_model_by_score(features)
    chosen_quality = get_model_info(chosen)["quality_score"]
    assert chosen_quality >= 0.85