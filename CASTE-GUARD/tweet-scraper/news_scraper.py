import requests
import json

API_KEY = "1d6fec3f1c434ad689ff5ec6a3a88ff8"  # <-- Replace this with your key
QUERY = 'dalit OR caste OR reservation OR untouchability OR manual scavenging'
URL = f"https://newsapi.org/v2/everything?q={QUERY}&language=en&sortBy=publishedAt&apiKey={API_KEY}"

print("🔍 Fetching latest caste-related news...")

response = requests.get(URL)

if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])
    
    # Save to JSON
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(articles)} articles to 'news.json'")
else:
    print("❌ Failed to fetch news:", response.status_code)
    print(response.text)