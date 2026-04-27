import feedparser
from datetime import datetime, timedelta
import requests

BOT_TOKEN = "8634009414:AAFUH0gzMKYdr2RglHHj3A_3GQ4GMdbfeHY"
CHAT_ID = "46754785"

url = "https://news.google.com/rss/search?q=신천지&hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(url)

# 📅 전날 기준 (UTC 보정)
today = datetime.now()
yesterday_start = today - timedelta(days=1)

results = []

for entry in feed.entries:
    try:
        published = datetime(*entry.published_parsed[:6])

        # ✔ 전날 기사만 필터
        if published >= yesterday_start:

            title = entry.title
            link = entry.link

            # 🧠 카테고리 분류 (간단 버전)
            if "수사" in title or "고발" in title or "재판" in title:
                category = "사건/논란"
            elif "정부" in title or "정치" in title:
                category = "정치/사회"
            else:
                category = "기타"

            # 🧠 아주 간단한 요약 (제목 기반)
            summary = f"{title} 관련 주요 기사입니다."

            results.append(f"[{category}]\n{title}\n{summary}\n{link}\n")

    except:
        continue

text = "\n\n".join(results) if results else "전날 기사 없음"

with open("news.txt", "w", encoding="utf-8") as f:
    f.write(text)

with open("news.txt", "rb") as f:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data={"chat_id": CHAT_ID},
        files={"document": f}
    )
