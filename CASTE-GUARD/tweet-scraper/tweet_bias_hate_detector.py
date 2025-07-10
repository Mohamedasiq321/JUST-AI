# tweet_bias_hate_detector.py
import json
import csv
import re
from transformers import pipeline

# Load your latest tweet file (change filename accordingly)
filename = "live_tweets_YYYY-MM-DD_HH-MM-SS.json"  # Replace with real filename

with open(filename, "r", encoding="utf-8") as f:
    tweets = json.load(f)

# Load hate detection pipeline
hate_classifier = pipeline("text-classification", model="unitary/toxic-bert")

# Define caste-related biased patterns
bias_keywords = [
    r"\b(dalit|lower caste|reservation|quota|sc/st|backward class|caste)\b",
    r"\b(get everything|free seats|undeserving|stupid|dirty)\b",
    r"\b(manual scavenging|untouchable|slur)\b"
]

def is_biased(text):
    for pattern in bias_keywords:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

# Analyze & Save flagged tweets
flagged = []

for tweet in tweets:
    text = tweet.get("text", "")
    bias = is_biased(text)
    hate_score = hate_classifier(text)[0]['score'] if bias else 0

    if bias or hate_score > 0.5:
        flagged.append({
            "text": text,
            "hate_score": round(hate_score, 4),
            "bias": bias
        })

# Save to CSV
with open("flagged_tweet_bias.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "hate_score", "bias"])
    writer.writeheader()
    writer.writerows(flagged)

print(f"✅ Done! Flagged {len(flagged)} tweets saved to 'flagged_tweet_bias.csv'")
