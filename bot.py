import feedparser
from datetime import datetime, timedelta
import requests

BOT_TOKEN = "8634009414:AAFUH0gzMKYdr2RglHHj3A_3GQ4GMdbfeHY"
CHAT_ID = "409793150"

url = "https://news.google.com/rss/search?q=신천지&hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(url)

# 🔥 테스트용: 7일로 늘림
yesterday = datetime.now() - timedelta(days=7)

results = []

for entry in feed.entries:
    results.append(f"{entry.title}\n{entry.link}")

text = "\n\n".join(results)

print("RESULT COUNT:", len(results))  # 로그 확인용

with open("news.txt", "w", encoding="utf-8") as f:
    f.write(text)

with open("news.txt", "rb") as f:
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data={"chat_id": CHAT_ID},
        files={"document": f}
    )

print("Telegram response:", r.text)
