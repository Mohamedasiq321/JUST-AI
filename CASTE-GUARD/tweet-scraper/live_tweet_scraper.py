# live_tweet_scraper.py
import requests
import json
from datetime import datetime
import os

# Your Bearer Token goes here
BEARER_TOKEN = "YOUR_BEARER_TOKEN_HERE"  # 🔒 Don't commit this if uploading anywhere!

# Define your search query
SEARCH_QUERY = "caste OR untouchability OR dalit OR caste-based violence lang:en -is:retweet"

# Define headers for the Twitter API
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "CASTE-GUARD-TweetScraper"
}

# Endpoint for recent tweets
url = "https://api.twitter.com/2/tweets/search/recent"

# Set parameters
params = {
    "query": SEARCH_QUERY,
    "max_results": 50,  # Up to 100
    "tweet.fields": "created_at,text,author_id"
}

# Call the API
print("🔍 Fetching tweets from Twitter...")
response = requests.get(url, headers=headers, params=params)

if response.status_code != 200:
    print(f"❌ Error: {response.status_code} - {response.text}")
else:
    data = response.json()
    tweets = data.get("data", [])

    # Save the tweets into a file
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"live_tweets_{now}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tweets, f, indent=4, ensure_ascii=False)

    print(f"✅ {len(tweets)} tweets saved to '{output_file}'")
