import asyncio
from typing import Optional
import discord
import aiohttp
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
block_users = [917030705870028901, 1042790192307781642]

async def global_check(ctx):
    # 차단된 유저 리스트에 있는지 확인
    return ctx.author.id not in block_users

bot.add_check(global_check) 


# 명령어 실행 실패(특히 CheckFailure)에 대한 에러 핸들링
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f'죄송하지만, {ctx.author.mention}, 당신은 이 명령어를 사용할 수 없습니다.\n사유 :  후원자 전용 명령어 또는 시스탬 오류')
        print(Color.RED + f"the blacklist user {ctx.author} failed to use a commands" + Color.RESET)
    else:
        print(f'Unhandled error: {error}')

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

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx : commands.context, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{amount}개의 메시지를 삭제했습니다.', delete_after=5)

@bot.command(name="새벽맨션")
async def mention_late(ctx : commands.context):
    user = ctx.author
    role_name = "새벽맨션"
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        # 사용자가 이미 해당 역할을 가지고 있는지 확인합니다.
        if role in user.roles:
            await ctx.send(f'이미 규칙을 갖고 있습니다.. {role_name}')
        else:
            # 역할을 부여합니다.
            await user.add_roles(role)
            await ctx.send(f'{role_name} 이 지급되었습니다..!')
    else:
        await ctx.send(f'{role_name} 이 이미 존제하지 않습니다.')


'''
@bot.event
async def on_error(event, *args, **kwargs):
    exc_info = traceback.format_exc()
    print(Color.RED+f"{now}     [ERROR] {event} - {args} - {kwargs}"+ Color.RESET)
    print(Color.RED+f"{exc_info}"+Color.RESET)

'''
bot.run(token)
