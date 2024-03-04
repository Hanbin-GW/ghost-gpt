import asyncio
from typing import Optional
import discord
from color_ansi import Color
from discord.ext import commands
from config.config import *
import os
import datetime
import psutil
#from random import random
from datetime import datetime
now = datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
intents = discord.Intents.all()
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents, owner_ids=[759072684461391893])  # 봇의 접두사 설정
# 로깅 초기화
#logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
class HelpView(discord.ui.View):
    def __init__(self, help_command, cogs):
        super().__init__()
        self.help_command = help_command
        self.cogs = cogs

        # 각 코그에 대한 버튼 추가
        for cog_name in cogs:
            self.add_item(discord.ui.Button(label=cog_name, style=discord.ButtonStyle.primary))

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger)
    async def close_button(self, interaction, button):
        await interaction.response.defer()
        await interaction.delete_original_message()

    async def interaction_check(self, interaction):
        # 버튼 클릭 이벤트 처리
        for child in self.children:
            if child.label != "Close" and interaction.data["custom_id"] == child.custom_id:
                await interaction.response.edit_message(content=None, embed=await self.help_command.get_cog_help(child.label))
                return True
        return False

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        destination = self.get_destination()
        cogs = [cog.qualified_name for cog in self.context.bot.cogs.values()]
        view = HelpView(self, cogs)
        await destination.send("Select a category:", view=view)

    async def get_cog_help(self, cog_name):
        # 특정 코그에 대한 도움말을 생성하는 함수
        cog = self.context.bot.get_cog(cog_name)
        if cog is None:
            return discord.Embed(title="Error", description="No such cog.", color=discord.Color.red())
        embed = discord.Embed(title=f"{cog_name} Commands", description="\n".join([f"`{command.name} : {command.description}`" for command in cog.get_commands()]))
        
        return embed
        #return discord.Embed(title=f"{cog_name} Commands", description="\n".join([f"`{command.name} : {command.description}`" for command in cog.get_commands()]))

bot.help_command = MyNewHelp()

async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            
            #print(f"{now}   INFO: {filename} --> online")
            print(f"{Color.GREEN}{now}{Color.RESET}{Color.BLUE} {Color.BOLD}INFO     {Color.MAGENTA}{filename} --> online{Color.RESET}")
            await bot.load_extension(f"cogs.{filename[:-3]}")
@bot.event
async def on_ready():  # 봇 준비 시 1회 동작하는 부분
    # 봇 이름 하단에 나오는 상태 메시지 설정
    #await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("host : 127.0.0.1"))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("host : synology NAS"))
    print(Color.BLUE+"Bot is ready"+Color.RESET)
    print(f"{Color.BLUE}{len(bot.guilds)} server joined\n{Color.RESET}")
    await setup_hook()

@bot.command()
async def stats(ctx):
    bedem = discord.Embed(title = 'System Resource Usage', description = 'See CPU and memory usage of the system.')
    bedem.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
    bedem.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
    bedem.add_field(name = 'Available Memory', value = f'{psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}%', inline = False)
    await ctx.send(embed = bedem)

'''
@bot.event
async def on_error(event, *args, **kwargs):
    exc_info = traceback.format_exc()
    print(Color.RED+f"{now}     [ERROR] {event} - {args} - {kwargs}"+ Color.RESET)
    print(Color.RED+f"{exc_info}"+Color.RESET)

'''
bot.run(token)
