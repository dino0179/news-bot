import feedparser
from datetime import datetime, timedelta
import requests

BOT_TOKEN = "8634009414:AAFUH0gzMKYdr2RglHHj3A_3GQ4GMdbfeHY"
CHAT_ID = "46754785"

url = "https://news.google.com/rss/search?q=신천지&hl=ko&gl=KR&ceid=KR:ko"
feed = feedparser.parse(url)

# 📅 전날 기준 (UTC 고려해서 2일 여유)
cutoff = datetime.now() - timedelta(days=2)

categories = {
    "사건/논란": [],
    "정치/사회": [],
    "기타": []
}

for entry in feed.entries:
    try:
        published = datetime(*entry.published_parsed[:6])

        if published >= cutoff:
            title = entry.title
            link = entry.link

            # 🧠 간단 카테고리 분류
            if any(word in title for word in ["수사", "재판", "고발", "압수", "조사"]):
                cat = "사건/논란"
            elif any(word in title for word in ["정부", "정치", "국회", "여당", "야당"]):
                cat = "정치/사회"
            else:
                cat = "기타"

            categories[cat].append(f"- {title}\n  {link}")

    except:
        continue

# 📦 텍스트 메시지 생성
message = ""

for cat, items in categories.items():
    if items:
        message += f"[{cat}]\n" + "\n".join(items) + "\n\n"

if not message:
    message = "전날 뉴스 없음"

# 📲 텔레그램 전송 (파일 X, 텍스트 O)
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
