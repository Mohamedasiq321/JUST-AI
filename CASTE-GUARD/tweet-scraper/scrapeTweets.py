# tweet-scraper/scrapeTweets.py

import subprocess
import json
import sys

def scrape_tweets(keyword, max_results=5):
    command = [
        "snscrape",
        "--jsonl",
        f"--max-results={max_results}",
        "twitter-search",
        f"{keyword}"
    ]

    try:
        output = subprocess.check_output(command, text=True)
        tweets = [json.loads(line)["content"] for line in output.strip().split('\n')]
        return tweets
    except subprocess.CalledProcessError as e:
        print("Error scraping tweets:", e)
        return []

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "dalit"
    tweets = scrape_tweets(keyword)
    print(json.dumps(tweets, indent=2))
