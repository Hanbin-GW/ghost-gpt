import discord
from discord.ext import commands
from discord import app_commands
from color_ansi import Color
import traceback
import openai
import aiohttp
from config.config import *
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(api_key="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")
#openai.base_url = "https://api.openai.com/v1/chat/completions"
#openai.default_headers = {"x-foo": "true"}
now = datetime.now()
now.strftime("%Y-%m-%d %H:%M:%S")


def code_respose(prompt):
    completion = client.completions.create(
        model="code-davinci-003",
        #prompt=prompt,
        messages =[
            {"role":"user","content":prompt}
        ],
        temperature=0.7
    )
    return completion.choices[0].message.content

def gpt_3_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    return completion.choices[0].message.content

def gpt_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4-0613",
        #model="gpt-4",
        #response_format={ "type": "json_object" },
        messages=[
            {"role": "user", "content": prompt},
        ],
        #max_tokens=8192
    )
    return completion.choices[0].message.content

def gpt_4_t_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        
        messages=[
            {"role":"user","content":prompt}
        ],
        max_tokens=4096,
        
    )
    return completion.choices[0].message.content

def gpt_4t_image(prompt , link):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages = [
            {
                "role": "user",
                "content" : [
                    {"type":"text","text":prompt},
                    {
                        "type":"image_url",
                        "image_url" : {"url": link}
                    }
                ]
            }
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

modlist = [759072684461391893]

def ListCheck():
    async def IsInList(ctx):
        member=ctx.message.author.id
        return member in modlist
    return commands.check(IsInList)

class Chat_gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="prototype gpt")
    @commands.is_owner()
    async def test(self,ctx : commands.context,*,prompt:str,link):
        response = gpt_4t_image(prompt,link)
        await ctx.reply(response)

    @app_commands.command(description="talk with GPT-4 : )")
    async def gpt_4(self,interaction : discord.Integration,*,prompt: str):
        await interaction.defer()
        await asyncio.sleep(40)
        response = gpt_response(prompt)
        await interaction.respond.send_message(response)
    
    
    @commands.hybrid_command(description="talk with GPT-4 : )")
    async def gpt(self,ctx : commands.context,*,prompt: str):
        async with ctx.typing():
            response = gpt_response(prompt)
            print(f"{Color.MAGENTA}{response}{Color.RESET}")
            await ctx.reply(response)

    @commands.command(name="gpt_4t",description="Moel : gpt-4-vision-preview")
    async def gpt4(self, ctx:commands.context,*,prompt:str):
        async with ctx.typing():
            response=gpt_4_t_response(prompt)
            print(f"{Color.MAGENTA}{response}{Color.RESET}")
            await ctx.reply(response)
    
    @commands.Cog.listener("on_message")
    async def on_message(self,message):
        if message.author.bot or message.content.startswith('$gpt'):
            return
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        prompt = user_message
        print(username + " said " + user_message.lower() + " in " + channel)
        
        #print(username + " said " + user_message.lower() + " in " + channel)

        if message.channel.name == '📱chat-gpt':
            async with message.channel.typing():
                respond = gpt_response(prompt)
                print(f"{Color.MAGENTA}{respond}{Color.RESET}")
                await message.channel.send(respond)

        if message.channel.name == "gpt-3":
            async with message.channel.typing():
                respond = await gpt_3_response(prompt)
                await message.channel.send(respond)

        if message.channel.name == "code-davinci-003":
            async with message.channel.typing():
                respond_c = await code_respose(prompt)
                await message.channel.send(respond_c)
        
        if message.channel.name == "gpt-4-turbo":
            async with message.channel.typing():
                respond = gpt_4_t_response(prompt)
                await message.channel.send(respond)

    
    @gpt.error
    async def error_gpt(self, ctx,error):
        await ctx.reply(error)

    @commands.Cog.listener()
    async def on_error(error, ctx:commands.context):
        await ctx.reply(error)

    '''
    @commands.Cog.listener("on_error")
    async def on_error(self,event, *args, **kwargs):
        exc_info = traceback.format_exc()
        print(Color.RED+ Color.BOLD+f"[ERROR] {event} - {args} - {kwargs}"+ Color.RESET +Color.RESET)
        print(Color.RED+f"{exc_info}"+Color.RESET)
    '''
async def setup(bot): 
    await bot.add_cog(Chat_gpt(bot))
