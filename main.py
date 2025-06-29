import discord
import asyncio
from config import DISCORD_BOT_TOKEN, CHANNEL_ID
from qiitaFetcher import get_qiita_articles
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
        msg = get_qiita_articles(tag=None, num=10)
        if msg:
            await channel.send("【Qiita 新着記事ピックアップ】\n" + msg)
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
        msg = get_qiita_articles(tag=tag, num=10)
        if msg:
            await message.channel.send("【Qiitaピックアップ】\n" + msg)
        else:
            await message.channel.send("記事が取得できませんでした。")

client.run(DISCORD_BOT_TOKEN)
