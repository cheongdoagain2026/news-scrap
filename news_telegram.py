import os
import json
import requests

KEYWORDS = ["청도", "박권현"]
SEEN_FILE = "seen_ids.json"

NAVER_CLIENT_ID = os.environ["NAVER_CLIENT_ID"]
NAVER_CLIENT_SECRET = os.environ["NAVER_CLIENT_SECRET"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

API_URL = "https://naverapihub.apigw.ntruss.com/search/v1/news"
HEADERS = {"X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID, "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET}


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def clean(text):
    return text.replace("<b>", "").replace("</b>", "").replace("&quot;", '"').replace("&amp;", "&")


def send(keyword, item):
    body = "[" + keyword + "] " + clean(item["title"]) + "\n" + item["pubDate"] + "\n" + item["link"]
    url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": body}, timeout=10)


seen = load_seen()
new_count = 0

for keyword in KEYWORDS:
    sent_links = seen.get(keyword, [])
    params = {"query": keyword, "display": 20, "sort": "date", "format": "json"}
    res = requests.get(API_URL, headers=HEADERS, params=params, timeout=10)
    res.raise_for_status()
    items = res.json().get("items", [])

    fresh = [it for it in items if it["link"] not in sent_links]
    for item in reversed(fresh):
        send(keyword, item)
        sent_links.append(item["link"])
        new_count += 1

    seen[keyword] = sent_links[-300:]

with open(SEEN_FILE, "w", encoding="utf-8") as f:
    json.dump(seen, f, ensure_ascii=False, indent=2)

print("신규 기사", new_count, "건 전송 완료")
