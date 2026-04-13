import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

# This tells the bot to look at your Railway Variables for the secret code
TOKEN = os.getenv('MTQ2NTc0MTY3NjYwODc1MzkyNg.Gqzegr.gr7ONnIAD_vTzbuEYDS5Tu8O2O6Hz9cTukXHKo')
VOICE_CHANNEL_ID = 1490460191651659850

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True 

bot = commands.Bot(command_prefix='!', intents=intents)

YTDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True', 'quiet': True}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f"✅ UltimateX Radio is LIVE")
        except Exception as e:
            print(f"❌ Connection error: {e}")

@bot.command()
async def play(ctx, *, url):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            return await ctx.send("You need to be in a VC first!")
    
    async with ctx.typing():
        info = ytdl.extract_info(url, download=False)
        url2 = info['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)
    await ctx.send(f'🎶 Now playing: **{info["title"]}**')

bot.run(TOKEN)
