from transformers import pipeline
import json
from tqdm import tqdm

# Load pre-processed tweet data
with open("analyzed_tweets.json", "r", encoding="utf-8") as file:
    tweets_data = json.load(file)

# Load zero-shot-classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# 🧠 Define your own custom intent categories
candidate_labels = [
    "hate speech",
    "caste discrimination",
    "religious hate",
    "political hate",
    "neutral",
    "supportive"
]

print("🔍 Starting intent classification...")
for tweet in tqdm(tweets_data):
    text = tweet.get("cleaned_text") or tweet.get("text") or ""
    if not text.strip():
        tweet["intent"] = "unknown"
        continue

    try:
        result = classifier(text, candidate_labels)
        tweet["intent"] = result["labels"][0]  # top predicted intent
        print(f"Text: {text}\nIntent: {tweet['intent']}\n")
    except Exception as e:
        print(f"Error on text: {text[:50]}... => {e}")
        tweet["intent"] = "unknown"

# Save updated data back to JSON
with open("analyzed_tweets.json", "w", encoding="utf-8") as file:
    json.dump(tweets_data, file, ensure_ascii=False, indent=2)

print("✅ Intent classification completed and saved.")