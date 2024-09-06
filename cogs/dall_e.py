import discord
from discord.ext import commands
from discord import app_commands
from color_ansi import Color
import requests
from dotenv import load_dotenv
import asyncio
from openai import OpenAI
load_dotenv()
from config.config import *
client = OpenAI(api_key=str(key))

allow_list = [1048458483311317053, 759072684461391893]

def ListCheck():
    async def IsInList(ctx):
        member=str(ctx.message.author.id)
        if member is allow_list:
            return True
        else:
            return False
    return commands.check(IsInList)

@commands.check
async def whitelist_channels(ctx):
    return str(ctx.channel) in allow_list

class dall_E(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="generate_image_legacy",description="Model : Dall-E-2")
    async def generate_image(self, ctx : commands.context, *, prompt:str):
        async with ctx.typing():
            response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            n=1,
            size="512x512",
            style="vivid"
        )
        image_url = response.data[0].url
        print(f"{Color.BLUE}{image_url}{Color.RESET}")
        image_response = requests.get(image_url)
        filename = "generated_image.png"

        with open(filename, "wb") as file:
            file.write(image_response.content)

        # 다운로드한 이미지를 Discord에 업로드합니다.
        with open(filename, "rb") as file:
            await ctx.reply(file=discord.File(file, filename))

    @commands.command(name="generate_image",description="Model : Dall-E-3")
    @commands.cooldown(1, 10800, commands.BucketType.user)
    async def generate_image_4k(self, ctx : commands.context, *, prompt:str):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            quality = "standard",
            n=1,
            size="1024x1024",
            style="vivid"
        )
        image_url = response.data[0].url
        print(f"{Color.BLUE}{image_url}{Color.RESET}")
        image_response = requests.get(image_url)
        filename = "generated_image.png"

        with open(filename, "wb") as file:
            file.write(image_response.content)

        # 다운로드한 이미지를 Discord에 업로드합니다.
        with open(filename, "rb") as file:
            await ctx.reply(file=discord.File(file, filename))

    @commands.command(name="generate_image_premium",description="Model : Dall-E-3")
    @commands.is_owner()
    #@commands.cooldown(1, 10800, commands.BucketType.user)
    async def generate_image_p(self, ctx : commands.context, *, prompt:str):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            n=1,
            quality="hd",
            style="vivid"
        )
        image_url = response.data[0].url
        print(f"{Color.BLUE}{image_url}{Color.RESET}")
        image_response = requests.get(image_url)
        filename = "generated_image.png"

        with open(filename, "wb") as file:
            file.write(image_response.content)

        # 다운로드한 이미지를 Discord에 업로드합니다.
        with open(filename, "rb") as file:
            await ctx.reply(file=discord.File(file, filename))

    

    @generate_image.error
    async def my_command_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Command is on cooldown, try again in {error.retry_after:.2f} seconds.')
        else:
            await ctx.send(error)
    '''
    @commands.command(name='gi',description="Dall-E-3 limited Acess")
    async def genetate(self, ctx : commands.Context, * ,prompt:str):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n = 1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        print(f"{Color.BLUE}{image_url}{Color.RESET}")
        image_response = requests.get(image_url)
        filename = "generated_image.png"

        with open(filename, "wb") as file:
            file.write(image_response.content)

        # 다운로드한 이미지를 Discord에 업로드합니다.
        with open(filename, "rb") as file:
            await ctx.reply(file=discord.File(file, filename))'''

async def setup(bot): # this is called by Pycord to setup the cog
    await bot.add_cog(dall_E(bot))