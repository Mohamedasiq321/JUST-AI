import json

print("🔍 Inspecting analyzed_tweets.json...")

# Load JSON
with open("analyzed_tweets.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Support both old and new formats
if isinstance(data, dict) and "data" in data:
    tweets = data["data"]
elif isinstance(data, list):
    tweets = data
else:
    raise ValueError("❌ Unknown structure in analyzed_tweets.json")

print(f"📊 Total tweets loaded: {len(tweets)}")

# Show the first tweet (full object)
print("\n🧠 First tweet entry:")
print(json.dumps(tweets[0], indent=2, ensure_ascii=False))

# Optional: print all available keys
print("\n🔑 Available keys in tweet:")
print(tweets[0].keys())

# Optional: confirm intent field exists in most tweets
intent_count = sum(1 for tweet in tweets if "intent" in tweet)
print(f"\n✅ Tweets with 'intent' field: {intent_count}/{len(tweets)}")
