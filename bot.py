import feedparser
from datetime import datetime, timedelta
import requests

BOT_TOKEN = "8634009414:AAFUH0gzMKYdr2RglHHj3A_3GQ4GMdbfeHY"
CHAT_ID = "46754785"

sources = [
    "https://news.google.com/rss/search?q=신천지&hl=ko&gl=KR&ceid=KR:ko",
    "https://newssearch.naver.com/search.naver?where=rss&query=신천지"
]

cutoff = datetime.utcnow() - timedelta(days=1)

politics = []
religion = []

# 🔥 종교 키워드 (강하게 제한)
religion_keywords = [
    "신천지", "이단", "사이비", "교회", "목회", "종교", "이만희", "구원파"
]

# 🔥 정치 키워드
politics_keywords = [
    "정부", "국회", "여당", "야당", "정책", "대통령", "법안", "선거"
]

for url in sources:
    feed = feedparser.parse(url)

    for entry in feed.entries:
        try:
            published = datetime(*entry.published_parsed[:6])

            if published >= cutoff:

                title = entry.title
                summary = entry.get("summary", "")
                text = (title + " " + summary).lower()

                link = entry.link

                # -------------------------
                # 1. 종교 (신천지/이단/사이비)
                # -------------------------
                if any(k in text for k in religion_keywords):
                    religion.append(f"- {title}\n  {link}")

                # -------------------------
                # 2. 정치
                # -------------------------
                elif any(k in text for k in politics_keywords):
                    politics.append(f"- {title}\n  {link}")

        except:
            continue

# -------------------------
# 메시지 생성
# -------------------------
message = ""

if politics:
    message += "[정치]\n" + "\n".join(politics) + "\n\n"

if religion:
    message += "[종교 - 신천지/이단/사이비]\n" + "\n".join(religion) + "\n\n"

if not message:
    message = "전날 관련 뉴스 없음"

# -------------------------
# 전송
# -------------------------
requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)
