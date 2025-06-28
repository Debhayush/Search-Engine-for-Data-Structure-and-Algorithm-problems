import os
import math
from collections import Counter
import re
from num2words import num2words

DATA_DIR = "data"
PROBLEM_DIR = os.path.join(DATA_DIR, "problemdata")

# Stopwords
STOPWORDS = set([
    "the", "is", "in", "to", "a", "an", "of", "for", "and", "on", "with", "that", "as", "are", "was",
    "this", "it", "be", "or", "from", "by", "at", "if", "then", "can", "we", "you", "your", "i", "but",
    "have", "has", "had", "not", "do", "does", "did", "so", "such", "these", "those", "he", "she", "they"
])

# --- Cleaning function ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    cleaned = []
    for token in tokens:
        if token in STOPWORDS:
            continue
        if token.isdigit():
            cleaned.extend(num2words(token).split())
        else:
            cleaned.append(token)
    return cleaned

# --- Step 1: Read and clean all documents ---
docs_tokens = []
all_tokens = set()

file_list = sorted(os.listdir(PROBLEM_DIR), key=lambda x: int(re.findall(r'\d+', x)[0]))

for filename in file_list:
    filepath = os.path.join(PROBLEM_DIR, filename)
    with open(filepath, encoding="utf-8") as f:
        tokens = clean_text(f.read())
        docs_tokens.append(tokens)
        all_tokens.update(tokens)

# --- Step 2: Build vocabulary ---
keywords = sorted(all_tokens)
word_to_index = {word: idx for idx, word in enumerate(keywords)}
num_docs = len(docs_tokens)
num_keywords = len(keywords)

# --- Step 3: Compute IDF ---
df = [0] * num_keywords
for tokens in docs_tokens:
    unique_tokens = set(tokens)
    for token in unique_tokens:
        df[word_to_index[token]] += 1

idf = [math.log(num_docs / df[i]) if df[i] != 0 else 0 for i in range(num_keywords)]

# --- Step 4: Write keywords.txt and IDF.txt ---
with open(os.path.join(DATA_DIR, "keywords.txt"), "w", encoding="utf-8") as f:
    for word in keywords:
        f.write(word + "\n")

with open(os.path.join(DATA_DIR, "IDF.txt"), "w", encoding="utf-8") as f:
    for val in idf:
        f.write(f"{val}\n")

# --- Step 5: Write TFIDF.txt ---
with open(os.path.join(DATA_DIR, "TFIDF.txt"), "w", encoding="utf-8") as f:
    for doc_id, tokens in enumerate(docs_tokens):
        tf = Counter(tokens)
        total_tokens = sum(tf.values())
        for word, count in tf.items():
            idx = word_to_index[word]
            tf_val = count / total_tokens
            tfidf = tf_val * idf[idx]
            f.write(f"{doc_id + 1} {idx} {tfidf}\n")

# --- Step 6: Write Magnitude.txt ---
with open(os.path.join(DATA_DIR, "Magnitude.txt"), "w", encoding="utf-8") as f:
    for doc_id, tokens in enumerate(docs_tokens):
        tf = Counter(tokens)
        total = sum(tf.values())
        norm_sq = 0
        for word, count in tf.items():
            idx = word_to_index[word]
            tf_val = count / total
            tfidf_val = tf_val * idf[idx]
            norm_sq += tfidf_val ** 2
        magnitude = math.sqrt(norm_sq)
        f.write(f"{magnitude}\n")

print("All files successfully regenerated:")
print(" - TFIDF.txt")
print(" - IDF.txt")
print(" - Magnitude.txt")
print(" - keywords.txt")