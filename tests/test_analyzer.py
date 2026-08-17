from analyzer import analyze_request, has_code, has_reasoning_keywords


def test_short_query_word_count():
    features = analyze_request("Bonjour")
    assert features["word_count"] == 1


def test_long_query_word_count():
    features = analyze_request("Ceci est une phrase avec plusieurs mots dedans")
    assert features["word_count"] == 8


def test_has_code_detects_python_def():
    assert has_code("def hello():") == True


def test_has_code_returns_false_for_plain_text():
    assert has_code("Bonjour comment vas-tu") == False


def test_has_reasoning_keywords_detects_analyse():
    assert has_reasoning_keywords("Analyse ce document") == True


def test_has_reasoning_keywords_returns_false_for_simple_text():
    assert has_reasoning_keywords("Bonjour") == False