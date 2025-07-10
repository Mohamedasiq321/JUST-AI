import json
import csv
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Set device (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device set to use {device}")

# Load model and tokenizer
MODEL = "unitary/toxic-bert"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.to(device)
model.eval()

# Load tweets
with open("tweets.json", "r", encoding="utf-8") as f:
    tweets_data = json.load(f)

tweets = tweets_data["data"]

def clean_text(text):
    # Remove URLs, mentions, hashtags, emojis
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    text = re.sub(r"#\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

analyzed = []
flagged = []

for tweet in tweets:
    cleaned = clean_text(tweet["text"])
    encoded = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        output = model(**encoded)
        scores = output.logits[0].cpu().numpy()
        probs = softmax(scores)
        hate_score = float(probs[2])  # 'toxic' is index 2 in this model
        result = {
            "text": tweet["text"],
            "cleaned_text": cleaned,
            "hate_score": round(hate_score, 4)
        }
        analyzed.append(result)
        if hate_score > 0.7:  # 💣 adjust to 0.7 or 0.8 if needed
            flagged.append(result)

# Save all analysis
with open("analyzed_tweets.json", "w", encoding="utf-8") as f:
    json.dump(analyzed, f, indent=2)

# Save only flagged (to CSV)
with open("flagged_hate_tweets.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "cleaned_text", "hate_score"])
    writer.writeheader()
    writer.writerows(flagged)

print("\n✅ Done!")
print(f"💾 All tweets analyzed -> analyzed_tweets.json")
print(f"🧹 Hateful tweets saved -> flagged_hate_tweets.csv (Total: {len(flagged)})")
