import requests
import random
from datetime import datetime

def get_qiita_articles(tag=None, num=10, raw=False):
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

    if raw:
        return items  # ← ここがポイント！

    pick_items = random.sample(items, min(num, len(items)))
    messages = []
    for i, item in enumerate(pick_items, 1):
        title = item["title"]
        page_url = item["url"]
        created_at = item["created_at"]
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        messages.append(f"**{i}. {title}**\n{page_url}\n投稿: {dt.strftime('%Y-%m-%d %H:%M')}\n")
    return "\n".join(messages)
    
def make_qiita_embeds(items, num=10):
    import discord
    pick_items = random.sample(items, min(num, len(items)))
    embeds = []
    for item in pick_items:
        title = item["title"]
        url = item["url"]
        description = item.get("body", "")[:120] + "..."  # 記事本文の最初だけ（HTML注意）
        thumbnail = item["user"].get("profile_image_url")
        author = item["user"]["id"]
        created_at = item["created_at"][:16].replace("T", " ")

        embed = discord.Embed(
            title=title,
            url=url,
            description=f"{description}\n\n投稿: {created_at} by {author}",
            color=discord.Color.green(),
        )
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        embeds.append(embed)
    return embeds
