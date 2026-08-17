def has_code(query: str) -> bool:
    """Détecte si la requête contient probablement du code"""
    code_keywords = ["def ", "class ", "function", "import ", "SELECT ", "```"]
    code_symbols = ["{", "}", ";", "()"]

    for keyword in code_keywords:
        if keyword in query:
            return True

    for symbol in code_symbols:
        if symbol in query:
            return True

    return False


def has_reasoning_keywords(query: str) -> bool:
    """Détecte des mots-clés qui suggèrent une tâche de raisonnement complexe"""
    reasoning_keywords = [
        "analyse", "analyser", "compare", "comparer",
        "explique en détail", "conçois", "conception",
        "pourquoi", "démontre", "prouve", "évalue",
        "design", "architecture", "algorithme"
    ]

    query_lower = query.lower()

    for keyword in reasoning_keywords:
        if keyword in query_lower:
            return True

    return False


def analyze_request(query: str):
    """Analyse la requête et retourne ses caractéristiques"""
    word_count = len(query.split())
    contains_code = has_code(query)
    contains_reasoning = has_reasoning_keywords(query)

    return {
        "word_count": word_count,
        "has_code": contains_code,
        "has_reasoning_keywords": contains_reasoning
    }