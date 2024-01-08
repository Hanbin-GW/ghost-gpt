import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix='!',intents = discord.Intents.all())

def get_player_count():
    # 실제 API 엔드포인트와 필요한 파라미터로 교체하세요
    api_url = f"http://api.scpslgame.com/serverinfo/121.166.155.25/7777.php"
    response = requests.get(api_url)
    if response.status_code == 200:
        try:
            return response.json().get('player_count','No data')
        except ValueError:
            return f"Error decoding JSON: {response.text}"
        else:
            return f"Error: Server responded with status code {response.status_code}"

    
    # JSON 응답에서 'player_count'가 필드라고 가정

@bot.event
async def on_ready():
    status = get_player_count()
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(status))

@bot.command()
async def playercount(ctx):
    count = get_player_count()
    await ctx.send(f"현재 플레이어 수는: {count}")

bot.run('MTEwNDkzMjQ1ODY5NDE4NTA0MQ.G78b48.POa_uEg4nVeQ4tb68hHEZyw0xUIToByFhoosXQ')
