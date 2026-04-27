import feedparser
from datetime import datetime, timedelta
import requests
import os

BOT_TOKEN = os.environ[8634009414:AAFUH0gzMKYdr2RglHHj3A_3GQ4GMdbfeHY]
CHAT_ID = os.environ[409793150]

url = "https://news.google.com/rss/search?q=신천지&hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(url)

yesterday = datetime.now() - timedelta(days=1)

results = []
for entry in feed.entries:
    published = datetime(*entry.published_parsed[:6])
    if published > yesterday:
        results.append(f"{entry.title}\n{entry.link}")

text = "\n\n".join(results)

with open("news.txt", "w", encoding="utf-8") as f:
    f.write(text)

with open("news.txt", "rb") as f:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data={"chat_id": CHAT_ID},
        files={"document": f}
    )
