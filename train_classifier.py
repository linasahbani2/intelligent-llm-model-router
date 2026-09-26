import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib


def load_data():
    with open("labeled_dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data]
    labels = [item["label"] for item in data]
    return texts, labels


def main():
    print("Chargement des données...")
    texts, labels = load_data()
    print(f"Total : {len(texts)} exemples\n")

    # --- Étape 1 : séparer entraînement / test ---
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels,
        test_size=0.2,
        random_state=42,
        stratify=labels
    )
    print(f"Entraînement : {len(X_train)} exemples")
    print(f"Test         : {len(X_test)} exemples\n")

    # --- Étape 2 : transformer le texte en nombres (TF-IDF) ---
    vectorizer = TfidfVectorizer(max_features=2000)
    X_train_vectors = vectorizer.fit_transform(X_train)
    X_test_vectors = vectorizer.transform(X_test)

    # --- Étape 3 : entraîner le classifieur ---
    print("Entraînement du classifieur...")
    classifier = LogisticRegression(max_iter=1000)
    classifier.fit(X_train_vectors, y_train)

    # --- Étape 4 : évaluer sur les données de test ---
    predictions = classifier.predict(X_test_vectors)
    accuracy = accuracy_score(y_test, predictions)

    print(f"\nPrécision sur les données de test : {accuracy:.3f}")
    print("\nRapport détaillé :")
    print(classification_report(y_test, predictions))

    # --- Étape 4bis : tester différents seuils de décision ---
    probabilities = classifier.predict_proba(X_test_vectors)
    classes = classifier.classes_
    complex_index = list(classes).index("complex")

    print("\n--- Test de différents seuils pour la classe 'complex' ---")
    for threshold in [0.5, 0.4, 0.35, 0.3, 0.25, 0.2]:
        custom_predictions = [
            "complex" if probabilities[i][complex_index] >= threshold else "simple"
            for i in range(len(probabilities))
        ]
        acc = accuracy_score(y_test, custom_predictions)
        report = classification_report(y_test, custom_predictions, output_dict=True, zero_division=0)
        complex_recall = report["complex"]["recall"]
        simple_recall = report["simple"]["recall"]
        complex_precision = report["complex"]["precision"]
        print(f"Seuil {threshold:.2f} → accuracy={acc:.3f} | recall(complex)={complex_recall:.3f} | precision(complex)={complex_precision:.3f} | recall(simple)={simple_recall:.3f}")

    # --- Étape 5 : sauvegarder le modèle entraîné ---
    joblib.dump(classifier, "ml_classifier.joblib")
    joblib.dump(vectorizer, "ml_vectorizer.joblib")
    print("\nModèle sauvegardé : ml_classifier.joblib, ml_vectorizer.joblib")


if __name__ == "__main__":
    main()