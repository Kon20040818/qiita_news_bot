import discord
import asyncio
from config import DISCORD_BOT_TOKEN, CHANNEL_ID
from qiitaFetcher import get_qiita_articles, make_qiita_embeds
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def daily_post():
    await client.wait_until_ready()
    while not client.is_closed():
        now = datetime.now()
        target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)
        channel = client.get_channel(CHANNEL_ID)
        items = get_qiita_articles(tag=None, num=10, raw=True)
        if items:
            embeds = make_qiita_embeds(items, num=10)
            await channel.send("【Qiita 新着記事ピックアップ】")
            for embed in embeds:
                await channel.send(embed=embed)
        else:
            await channel.send("記事が取得できませんでした。")

@client.event
async def on_ready():
    print(f"ログインしました: {client.user}")
    client.loop.create_task(daily_post())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!qiita'):
        parts = message.content.split()
        tag = parts[1] if len(parts) > 1 else None

        # Embed用に生データを取得
        items = get_qiita_articles(tag=tag, num=10, raw=True)
        if items:
            embeds = make_qiita_embeds(items, num=10)
            for embed in embeds:
                await message.channel.send(embed=embed)
        else:
            await message.channel.send("記事が取得できませんでした。")
client.run(DISCORD_BOT_TOKEN)
