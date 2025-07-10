import requests
import json

# Paste your real keys here (keep private!)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAGON0gEAAAAAN%2BD9s75BV69BnyJcc5QCP7nARqc%3DMEgcxKPz3ZkKGnTOx4FLiEEHmcCjC8B6R7OfAJW4PGU6byqJeZ"

# Search Query: You can update this dynamically based on your use-case
query = '("dalit" OR "caste" OR "reservation" OR "sc/st" OR "lower caste" OR "untouchability") lang:en -is:retweet'

# Twitter API Endpoint
url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=10&tweet.fields=author_id,created_at,text"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "CASTE-GUARD-Agent"
}

# Make the request
response = requests.get(url, headers=headers)

# Save to file (optional)
if response.status_code == 200:
    tweets = response.json()
    with open("tweets.json", "w", encoding="utf-8") as f:
        json.dump(tweets, f, indent=4, ensure_ascii=False)
    print("✅ Tweets fetched and saved to tweets.json")
else:
    print("❌ Failed to fetch tweets:", response.status_code)
    print(response.text)
