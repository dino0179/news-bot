import feedparser
from datetime import datetime, timedelta
import requests

# 🔐 본인 값 넣기
BOT_TOKEN = "8634009414:AAFUH0gzMKYdr2RglHHj3A_3GQ4GMdbfeHY"
CHAT_ID = "409793150"

url = "https://news.google.com/rss/search?q=신천지&hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(url)

# ⚠️ GitHub Actions는 UTC 기준이라 3일로 넉넉하게
yesterday = datetime.now() - timedelta(days=3)

results = []

for entry in feed.entries:
    try:
        published = datetime(*entry.published_parsed[:6])
        if published > yesterday:
            results.append(f"{entry.title}\n{entry.link}")
    except:
        continue

text = "\n\n".join(results) if results else "최근 뉴스 없음"

with open("news.txt", "w", encoding="utf-8") as f:
    f.write(text)

with open("news.txt", "rb") as f:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data={"chat_id": CHAT_ID},
        files={"document": f}
    )
