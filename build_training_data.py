from datasets import load_dataset
import json

COMPLEX_CATEGORIES = {"summarization", "brainstorming", "creative_writing"}

REASONING_KEYWORDS = [
    "analyse", "analyser", "compare", "comparer", "explique en détail",
    "conçois", "conception", "démontre", "prouve", "évalue",
    "design", "architecture", "algorithme", "explain in detail",
    "compare", "design", "analyze", "evaluate", "demonstrate"
]

LENGTH_THRESHOLD = 14  # 75e percentile du dataset


def has_reasoning_keywords(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in REASONING_KEYWORDS)


def label_complexity(example) -> str:
    instruction = example["instruction"]
    word_count = len(instruction.split())
    category = example["category"]

    if word_count > LENGTH_THRESHOLD:
        return "complex"
    if category in COMPLEX_CATEGORIES:
        return "complex"
    if has_reasoning_keywords(instruction):
        return "complex"

    return "simple"


def main():
    dataset = load_dataset("databricks/databricks-dolly-15k")
    train = dataset["train"]

    labeled_data = []
    for example in train:
        label = label_complexity(example)
        labeled_data.append({
            "text": example["instruction"],
            "label": label
        })

    simple_count = sum(1 for item in labeled_data if item["label"] == "simple")
    complex_count = sum(1 for item in labeled_data if item["label"] == "complex")

    print(f"Simple  : {simple_count}")
    print(f"Complex : {complex_count}")
    print(f"Total   : {len(labeled_data)}")

    with open("labeled_dataset.json", "w", encoding="utf-8") as f:
        json.dump(labeled_data, f, ensure_ascii=False, indent=2)

    print("\nSauvegardé dans labeled_dataset.json")


if __name__ == "__main__":
    main()