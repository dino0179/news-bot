import feedparser
from datetime import datetime
import requests

BOT_TOKEN = "8634009414:AAFUH0gzMKYdr2RglHHj3A_3GQ4GMdbfeHY"
CHAT_ID = "46754785"

url = "https://news.google.com/rss/search?q=신천지&hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(url)

results = [f"{e.title}\n{e.link}" for e in feed.entries]

text = "\n\n".join(results)

print("뉴스 개수:", len(results))

with open("news.txt", "w", encoding="utf-8") as f:
    f.write(text)

# 🔥 Telegram 응답까지 확인
with open("news.txt", "rb") as f:
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data={"chat_id": CHAT_ID},
        files={"document": f}
    )

print("Telegram 응답:", response.text)
