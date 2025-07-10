import json
import csv
import re

# Define caste-hate keywords for basic simulation
hate_keywords = [
    "dalit", "reservation", "sc st", "lower caste", "manual scavenging",
    "anti-reservation", "you people want reservation", "get everything for free",
    "caste hate", "caste discrimination"
]

# Load analyzed_tweets.json
with open("analyzed_tweets.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)

# Prepare output list
flagged = []

for tweet in tweets:
    text = tweet["text"].lower()
    hate_score = tweet.get("hate_score", 0)

    # Simulated intent logic
    if any(kw in text for kw in hate_keywords):
        if "against caste discrimination" in text or "support" in text:
            intent = "support"
        elif hate_score > 0.4:
            intent = "hate"
        else:
            intent = "neutral"
    else:
        intent = "unknown"

    # Add intent to tweet
    tweet["intent"] = intent

    # Save only those we flag as hateful
    if intent == "hate":
        flagged.append({
            "text": tweet["text"],
            "hate_score": round(hate_score, 4),
            "intent": intent
        })

# Save updated version
with open("analyzed_tweets.json", "w", encoding="utf-8") as f:
    json.dump(tweets, f, indent=2)

# Save flagged hate tweets
with open("flagged_hate_tweets.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "hate_score", "intent"])
    writer.writeheader()
    writer.writerows(flagged)

print(f"✅ Finished! Flagged {len(flagged)} hateful tweets saved to 'flagged_hate_tweets.csv'")