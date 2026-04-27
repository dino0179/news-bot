import feedparser
from datetime import datetime, timedelta
import requests

BOT_TOKEN = "8634009414:AAFUH0gzMKYdr2RglHHj3A_3GQ4GMdbfeHY"
CHAT_ID = "46754785"

# 🔗 Google + Naver RSS
sources = [
    "https://news.google.com/rss/search?q=신천지&hl=ko&gl=KR&ceid=KR:ko",
    "https://newssearch.naver.com/search.naver?where=rss&query=신천지"
]

cutoff = datetime.utcnow() - timedelta(days=1)

news_list = []

# ---------------------------
# 1. 수집
# ---------------------------
for url in sources:
    feed = feedparser.parse(url)

    for entry in feed.entries:
        try:
            published = datetime(*entry.published_parsed[:6])

            if published >= cutoff:
                title = entry.title
                link = entry.link

                news_list.append({
                    "title": title,
                    "link": link
                })

        except:
            continue

# ---------------------------
# 2. 중복 제거
# ---------------------------
seen = set()
unique_news = []

for n in news_list:
    if n["title"] not in seen:
        seen.add(n["title"])
        unique_news.append(n)

# ---------------------------
# 3. 중요도 점수 (간단 룰)
# ---------------------------
def score(title):
    keywords_high = ["수사", "압수", "재판", "고발", "정부", "논란"]
    keywords_mid = ["세미나", "교회", "목회", "종교"]

    if any(k in title for k in keywords_high):
        return 5
    elif any(k in title for k in keywords_mid):
        return 3
    else:
        return 2

for n in unique_news:
    n["score"] = score(n["title"])

# ---------------------------
# 4. 정렬 (중요도 순)
# ---------------------------
sorted_news = sorted(unique_news, key=lambda x: x["score"], reverse=True)

# ---------------------------
# 5. TOP 5
# ---------------------------
top_news = sorted_news[:5]

# ---------------------------
# 6. 메시지 생성
# ---------------------------
message = "[🔥 오늘 핵심 뉴스 TOP 5]\n\n"

for i, n in enumerate(top_news, 1):
    message += f"{i}. (중요도 {n['score']}/5)\n"
    message += f"{n['title']}\n"
    message += f"{n['link']}\n\n"

if not top_news:
    message = "오늘 핵심 뉴스 없음"

# ---------------------------
# 7. 전송
# ---------------------------
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
