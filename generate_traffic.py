import json
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "http://localhost:8000"
STRATEGIES = ["always_large", "rules", "score", "cascade", "ml"]


def load_queries():
    with open("labeled_dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return [item["text"] for item in data]


def main():
    n_requests = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    queries = load_queries()

    for i in range(1, n_requests + 1):
        query = random.choice(queries)
        strategy = random.choice(STRATEGIES)
        url = f"{BASE_URL}/route?" + urllib.parse.urlencode({"query": query, "strategy": strategy})

        start = time.perf_counter()
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                body = json.loads(response.read())
            elapsed = time.perf_counter() - start
            print(f"[{i}/{n_requests}] {strategy:<13} -> {body['chosen_model']:<7} ({elapsed:.2f}s)")
        except urllib.error.URLError as error:
            print(f"[{i}/{n_requests}] erreur : {error}")


if __name__ == "__main__":
    main()