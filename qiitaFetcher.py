import requests
import random
from datetime import datetime

def get_qiita_articles(tag=None, num=10):
    if tag:
        url = f"https://qiita.com/api/v2/tags/{tag}/items"
        params = {"per_page": 100}
    else:
        url = "https://qiita.com/api/v2/items"
        params = {"per_page": 100}

    response = requests.get(url, params=params)
    items = response.json()

    if not items:
        return None

    pick_items = random.sample(items, min(num, len(items)))
    messages = []
    for i, item in enumerate(pick_items, 1):
        title = item["title"]
        page_url = item["url"]
        created_at = item["created_at"]
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        messages.append(f"**{i}. {title}**\n{page_url}\n投稿: {dt.strftime('%Y-%m-%d %H:%M')}\n")
    return "\n".join(messages)
