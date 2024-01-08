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
client = OpenAI(api_key="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")


class dall_E(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="draw")
    async def generate(self, ctx:commands.context, *, prompt):
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
            }
        data = {
            "prompt": prompt,
            }
        response = requests.post('DALL·E_ENDPOINT_HERE', headers=headers, json=data)
        if response.status_code == 200:
            image_url = response.json()['image_url']
            await ctx.send(image_url)
        else:
            await ctx.send("Failed to generate image. Please try again.")

    @generate.error
    async def error(self,ctx,error):
        await ctx.reply(error)
    '''
    @app_commands.command(name="DallE_generate")
    @app_commands.choices(size = [
        discord.app_commands.choices(name="256x256",value=1),
        discord.app_commands.choices(name="512x512",value=2),
        discord.app_commands.choices(name="1024x1024",value=3)
    ])
    async def generate_command(self,size : str , ctx: commands.context,  *, prompt):
        #await ctx.respond("이미지가 나올때까지 시간이걸립니다...")
        try:
            await ctx.defer()
            await asyncio.sleep(40)
            response = openai.Image.create_variation(
                prompt = prompt,
                n=2,
                size = size
            )
            image_url = response['data'][0]['url']
            await ctx.respond(image_url)
            await ctx.send(f"\n{ctx.author.mention} 님 주문하신 {prompt} 그림 {size} 로 나오셧습니다~~")
        except discord.NotFound:
            print("Interaction이 이미 만료되었거나 존재하지 않습니다.")
    '''

    @commands.command(name="generate_image",description="Model : Dall-E-3")
    @commands.cooldown(1, 10800, commands.BucketType.user)
    async def generate_image(self, ctx : commands.context, *, prompt:str):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        #image_url = response.GetImageUrl()
        #image_url = response['data'][0]['url']
        #await ctx.reply(image_url)
        #await ctx.send("주위! 본 사진은 몇시간뒤 삭제됩니다!")
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
            raise error

async def setup(bot): # this is called by Pycord to setup the cog
    await bot.add_cog(dall_E(bot))