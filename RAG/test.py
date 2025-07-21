import pandas as pd
import requests
from sentence_transformers import SentenceTransformer
import time

# Load last 1000 rows of the CSV
df = pd.read_csv("../Merged Datasets/cleaned_dataset.csv").tail(750)

# Load Hugging Face embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')


# Use Ollama HTTP API for faster and stable response
def ollama_query(prompt: str, model: str = "herald/phi3-128k:latest", retries: int = 3) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}

    for attempt in range(retries):
        try:
            response = requests.post(url, json = payload, timeout = 60)
            response.raise_for_status()
            return response.json()['response'].strip()
        except Exception as e:
            print(f"⚠️ Ollama error (attempt {attempt + 1}): {e}")
            time.sleep(2)
    return ""


# Structured prompt to get both summary and keywords
def build_combined_prompt(content: str) -> str:
    return f"""
You are a helpful assistant. Given the following article content, do the following:

1. Summarize the content meaningfully in around 50 words.
2. Extract at least 3 important keywords from the content, formatted as a single comma-separated line.

Respond in this exact format:
Summary: <your summary here>
Keywords: <comma, separated, keywords>

CONTENT:
{content}
""".strip()


# Parse Ollama response
def parse_response(response: str):
    summary, keywords = "", ""
    for line in response.splitlines():
        if line.lower().startswith("summary:"):
            summary = line.partition(":")[2].strip()
        elif line.lower().startswith("keywords:"):
            keywords = line.partition(":")[2].strip()
    return summary, keywords


# Prepare lists
summaries, keywords_list, embeddings = [], [], []

# Process rows
# Process rows
for count, (_, row) in enumerate(df.iterrows(), start=1):
    print(f"Processing row {count} of {len(df)}")
    content = str(row['content'])[:4000]  # avoid overload
    prompt = build_combined_prompt(content)
    response = ollama_query(prompt)

    summary, keywords = parse_response(response)

    # Fallback if response is bad
    if not summary:
        summary = "Summary not generated."
    if not keywords:
        keywords = "N/A"

    # Embed the summary
    embedding = embed_model.encode(summary, convert_to_numpy = True).tolist()

    summaries.append(summary)
    keywords_list.append(keywords)
    embeddings.append(embedding)


# Add to DataFrame
df['summary'] = summaries
df['keywords'] = keywords_list
df['embedding'] = embeddings

# Save to new CSV
df.to_csv("../Merged Datasets/last_1494.csv", index = False)
print("✅ Done. Output saved to '../Merged Datasets/last_1494.csv'")
