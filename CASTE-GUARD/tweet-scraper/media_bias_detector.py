import json
import csv
import re

# Load scraped news articles
with open("news.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

print(f"📰 Loaded {len(articles)} news articles")

# Keywords to detect caste-linked bias
caste_keywords = [
    "dalit", "scavenging", "untouchable", "reservation", "quota", 
    "lower caste", "caste conflict", "atrocities", "oppressed", "backward caste"
]

# Bias-inducing tones
biased_phrases = [
    "violent", "raging", "clash", "mob", "terror", "stormed", "shocking", "hate", "anger", "explosive", "fanatic"
]

flagged = []

for article in articles:
    title = article.get("title", "")
    content = article.get("description", "") or ""
    full_text = f"{title} {content}".lower()

    caste_hits = any(k in full_text for k in caste_keywords)
    tone_hits = any(p in full_text for p in biased_phrases)

    if caste_hits and tone_hits:
        flagged.append({
            "title": article.get("title", "No title"),
            "source": article.get("source", {}).get("name", "Unknown"),
            "publishedAt": article.get("publishedAt", "N/A"),
            "url": article.get("url", "#")
        })

# Save results
with open("flagged_news_bias.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "source", "publishedAt", "url"])
    writer.writeheader()
    writer.writerows(flagged)

print(f"✅ Flagged {len(flagged)} caste-biased articles saved to 'flagged_news_bias.csv'")