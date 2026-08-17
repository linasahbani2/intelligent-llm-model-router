def analyze_request(query: str):
    """Analyse la requête et retourne ses caractéristiques"""
    word_count = len(query.split())
    return {
        "word_count": word_count
    }