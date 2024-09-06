import discord
from discord.ext import commands
from discord import app_commands
from color_ansi import Color
from config.config import *
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import base64
import requests
load_dotenv()
import os

client = OpenAI(api_key=str(new_key))
now = datetime.now()
now.strftime("%Y-%m-%d %H:%M:%S")
current_path = os.getcwd()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "path_to_your_image.jpg"

# Getting the base64 string

def gpto_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"user", "content":prompt},
        ]
    )
    return completion.choices[0].message.content

def gpt_3_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role":"user","content":prompt}
        ]
    )
    return completion.choices[0].message.content

def gpt_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        #model="gpt-4-turbo-preview"
        #response_format={ "type": "json_object" },
        messages=[
            {"role": "user", "content": prompt},
        ],
        #max_tokens=10000
    )
    return completion.choices[0].message.content

def gpt_4_t_response(prompt):
    completion = client.chat.completions.create(
        #model="gpt-4-0125-preview",
        model="gpt-4-turbo", 
        messages=[
            {"role":"user","content":prompt}
        ],
        max_tokens=4096,
        
    )
    return completion.choices[0].message.content

def gpt_4t_image(prompt, base64_image):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages = [
            {
                "role": "user",
                "content" : [
                    {"type":"text","text":prompt},
                    {
                        "type":"image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ]
            }
        ],
        max_tokens=300
    )
    #print(response.choices[0].message.content)
    return response.choices[0].message.content

modlist = [759072684461391893, 1048458483311317053, 1048458483311317053]

def ListCheck():
    async def IsInList(ctx):
        member=ctx.message.author.id
        if member is modlist:
            return True
        else:
            return False
    return commands.check(IsInList)

class Chat_gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="prototype gpt")
    @commands.is_owner()
    async def test(self,ctx : commands.context,prompt:str,link:str):
        response = gpt_4t_image(prompt,link)
        await ctx.reply(response)

    @app_commands.command(description="talk with GPT-4 : )")
    async def gpt_4(self,interaction : discord.Integration,*,prompt: str):
        await interaction.defer()
        await asyncio.sleep(40)
        response = gpt_response(prompt)
        await interaction.respond.send_message(response)
    
    
    @commands.hybrid_command(description="talk with GPT-4")
    async def gpt(self,ctx : commands.context,*,prompt: str):
        async with ctx.typing():
            response = gpt_response(prompt)
            print(f"{Color.MAGENTA}{response}{Color.RESET}")
            await ctx.reply(response)

    @commands.command(name="gpt_4t",description="Moel : gpt-4-vision-preview")
    @ListCheck()
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

        if message.channel.name == 'chat-gpt':
            async with message.channel.typing():
                respond = gpt_response(prompt)
                print(f"{Color.MAGENTA}{respond}{Color.RESET}")
                await message.channel.send(respond)

        if message.channel.name == "gpt-3":
            async with message.channel.typing():
                respond = await gpt_3_response(prompt)
                await message.channel.send(respond)



        if message.channel.name == "gpt-4-vision":
            if not message.attachments:
                async with message.channel.typing():
                    respond = gpt_4_t_response(prompt)
                    await message.channel.send(respond)
            if message.attachments:
                for attachment in message.attachments:
                # 이미지 파일인 경우에만 처리
                    if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['jpg', 'jpeg', 'png', 'gif']):
                        response = requests.get(attachment.url)

                    # 요청이 성공적이면 파일 저장
                        if response.status_code == 200:
                            #file_path = f"./saved_images/{attachment.filename}"
                            file_path = f"./saved_images/image.png"
                            #base64_image = encode_image({attachment.filename})
                            with open(file_path, 'wb') as f:
                                f.write(response.content)
                            print(f"Image saved: {file_path}")
                            #print(base64_image)
                            base64_image = encode_image(image_path=file_path)
                            respond = gpt_4t_image(prompt=prompt, base64_image=base64_image)
                            await message.channel.send(respond)
                            print(f"{Color.BLUE}Vision     {respond}{Color.RESET}")
                        else:
                            print("Failed to download the image.")
            

    
    @gpt.error
    async def error_gpt(self, ctx,error):
        await ctx.reply(error)
        
    @gpt4.error
    async def error_gpt4(self, ctx,error):
        await ctx.reply(error)

    @commands.Cog.listener()
    async def on_error(self, error, ctx:commands.context):
        await ctx.reply(error)

async def setup(bot): 
    await bot.add_cog(Chat_gpt(bot))
