import discord
from discord.ext import commands , tasks
from discord.commands import Option
from config.config import token,key
import aiohttp
import openai
from itertools import cycle
import asyncio
from dotenv import load_dotenv
from role import Verify
load_dotenv()

status = cycle(["use '$gpt' to talk ghost gpt!", "made bt hanbin#0939", "SCP : Secreat Laboratory","gpt_3.5","$help"])
bot = commands.Bot(command_prefix='$',intents=discord.Intents.all())
bot.remove_command("help")
openai.api_key = key
@bot.event
async def on_ready():
    print(f"[!] 다음으로 로그인에 성공했습니다.")
    print(f"[!] 다음 : {bot.user.name}")
    print(f"[!] 다음 : {bot.user.id}")
    print(f"[!] 참가 중인 서버 : {len(bot.guilds)}개의 서버에 참여 중\n") 
    change_status.start()

@tasks.loop(seconds=5)    # n초마다 다음 메시지 출력
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.command(name="help",help="show this commands")
async def help(ctx):
    embed = discord.Embed(title="help")
    file = discord.File("Ghosts_insignia_CoDG.png",filename="image.png")
    embed.set_author(name="command list",icon_url="attachment://image.png")
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name="$help",value="Shows this message",inline=False)
    embed.add_field(name="$gpt",value="ask a Chat-Gpt (model = text-davinci-003)",inline=False)
    embed.add_field(name="$gpt_3.5",value=" Ask __GPT-3.5-Turbo__ a question or send a message",inline=False)
    embed.add_field(name="/dev_role",value="you can get develoer community acess room.",inline=False)
    await ctx.reply(embed=embed,file=file)

@bot.command(guild_ids=[1069174895893827604],help="ask a chat-gpt")
async def gpt(ctx:commands.Context, *,prompt:str):
    async with ctx.typing():
        await asyncio.sleep(2)
    async with aiohttp.ClientSession() as session:
        response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=3000,
                temperature=0.7,
                )

        headers = {"Authorization" : f"banner{key}"}
        async with session.post("https://api.openai.com/v1/completions", json=response , headers=headers) as resp:
            output = response["choices"][0]["text"]
            embed = discord.Embed(title="chat GPT's response" , description=output,color=0xe6caff)
            print(output)
            await ctx.reply(embed=embed)

async def gpt_response(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

@bot.command(name="gpt_3.5", help="Ask GPT-3.5 Turbo a question or send a message")
async def gpt(ctx, *, prompt: str):
    async with ctx.typing():
        await asyncio.sleep(2)
    response = await gpt_response(prompt)
    await ctx.send(response)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1083242633310261298) # Where ID is your welcome channel's ID
    guild = bot.get_guild(1069174895893827604)
    role = guild.get_role(1072660369274843257)
    await member.add_roles(role)
    embed = discord.Embed(title="welcome",description='만나서 반가워요!! XD',color=0x1700ff)
    embed.set_thumbnail(url=member.avatar.url)
    await channel.send(f'{member.mention} 님 {member.guild.name} 서버에 오신것을 환영합니다!!!',embed=embed)

@bot.slash_command(guild_ids = [1069174895893827604])
async def dev_role(ctx,
            code:Option(str,"code type",choices=["python","java","c#","c",'Exiled'])):
    if code == "python":
        guild = bot.get_guild(1069174895893827604)
        role = guild.get_role(1084676732231098438)
        user = ctx.author
        await user.add_roles(role)
        await ctx.respond("you got a **python** role.")
    if code == "java":
        guild = bot.get_guild(1069174895893827604)
        role = guild.get_role(1084676808118644877)
        user = ctx.author
        await user.add_roles(role)
        await ctx.respond("you got a  **java** role.")

    if code == "c#":
        guild = bot.get_guild(1069174895893827604)
        role = guild.get_role(1084676863609294938)
        user = ctx.author
        await user.add_roles(role)
        await ctx.respond("you got a  **c#** role.")

    if code == "c":
        guild = bot.get_guild(1069174895893827604)
        role = guild.get_role(1084676940893532160)
        user = ctx.author
        await user.add_roles(role)
        await ctx.respond("you got a  **c** role.")
    if code == "Exiled":
        guild = bot.get_guild(1069174895893827604)
        role = guild.get_role(1085208002010824757)
        user = ctx.author
        await user.add_roles(role)
        await ctx.respond("you got a **exiled** role.")

@bot.command(name="welcome_embed")
@commands.is_owner()
async def test(ctx):
    embed = discord.Embed(title="welcome",description='만나서 반가워요!! XD',color=0xffffff)
    embed.set_thumbnail(url=ctx.author.avatar.url)
    embed.set_image(url='https://hub.scpslgame.com/images/thumb/1/12/HCZHIDSide.png/638px-HCZHIDSide.png')
    embed.set_footer(text="서버에 와주셔서 진심으로 감사드립니다",icon_url="https://th.bing.com/th/id/OIP.TPIH5vkBHW57cd7zyStnuAHaHa?pid=ImgDet&rs=1")
    await ctx.send(embed=embed)

@bot.command(name="verify")
async def v(ctx):
    await ctx.reply(view=Verify())

@test.error
async def test_error(error,ctx):
    await ctx.send("error detected\nreason\n",error)

bot.run(token)