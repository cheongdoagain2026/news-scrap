import requests

url = "http://chdonews.com/bbs/rss.php?bo_table=news"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

res = requests.get(url, headers=headers, timeout=15)
print("응답 코드:", res.status_code)
print("응답 앞 300자:", res.text[:300])

if res.status_code == 200 and "<item>" in res.text:
    count = res.text.count("<item>")
    print("기사 수:", count)
else:
    print("실패 - RSS 접근 불가")
