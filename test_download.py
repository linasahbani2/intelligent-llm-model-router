from datasets import load_dataset
import statistics

dataset = load_dataset("databricks/databricks-dolly-15k")
train = dataset["train"]

lengths = [len(example["instruction"].split()) for example in train]

print(f"Longueur moyenne : {statistics.mean(lengths):.1f} mots")
print(f"Longueur médiane : {statistics.median(lengths):.1f} mots")
print(f"Longueur min : {min(lengths)} mots")
print(f"Longueur max : {max(lengths)} mots")
print(f"25e percentile : {sorted(lengths)[len(lengths)//4]} mots")
print(f"75e percentile : {sorted(lengths)[3*len(lengths)//4]} mots")