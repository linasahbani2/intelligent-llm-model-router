import joblib

CLASSIFIER = joblib.load("ml_classifier.joblib")
VECTORIZER = joblib.load("ml_vectorizer.joblib")

COMPLEX_THRESHOLD = 0.50


def predict_complexity(query: str) -> str:
    """Utilise le modèle ML entraîné pour prédire si une requête est simple ou complexe"""
    query_vector = VECTORIZER.transform([query])
    probabilities = CLASSIFIER.predict_proba(query_vector)[0]

    classes = CLASSIFIER.classes_
    complex_index = list(classes).index("complex")
    complex_probability = probabilities[complex_index]

    if complex_probability >= COMPLEX_THRESHOLD:
        return "complex"
    else:
        return "simple"