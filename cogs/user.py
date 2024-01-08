import discord
from discord import app_commands 
from discord.ext import commands
from discord.utils import get
import datetime
import logging
#logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
#logger = logging.getLogger(__name__)

with open('blacklist.txt', 'r') as file:
    raw_blacklist = [line.strip().split(",") for line in file if "," in line]
    blacklist = {(int(server_id), int(user_id)) for server_id, user_id in raw_blacklist}

class Questionnaire(discord.ui.Modal, title='Questionnaire Response'):
    name = discord.ui.TextInput(label='Name')
    answer = discord.ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)

class user(commands.Cog):
    rules_message_id = 1084676435786084422

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        if (message.guild.id, message.author.id) in blacklist:
            await message.delete()
            return
    @app_commands.command()
    async def send_message(self, interaction:discord.Interaction, member: discord.User, *, message: str):
        await member.send(message)
        await interaction.response.send_message("message has been sent")


    @app_commands.command(name="profile")
    async def profile(self,interaction : discord.Interaction):
        member = interaction.user
        roles = [role for role in member.roles[1:]]
        embed = discord.Embed(title=f"{member}",color=0x929292)
        embed.add_field(name="**•ID•**", value=f"{member.id}", inline=True)
        embed.add_field(name="**•Status•**", value=str(member.status).replace("dnd", "Do Not Disturb"), inline=True)
        embed.set_thumbnail(url=f"{member.avatar.url}")
        embed.add_field(name=f"**•Roles• ({len(member.roles) - 1})**", value='• '.join([role.mention for role in roles]), inline=False)
        embed.add_field(name="**•Account Created At•**", value=f"{member.created_at.date()}".replace("-", "/"), inline=True)
        embed.add_field(name="**•Joined Server At•**", value=f"{member.joined_at.date()}".replace("-", "/"), inline = True)
        embed.set_footer(icon_url = f"{member.avatar.url}", text = f"Requested by {member}")
        embed.timestamp = datetime.datetime.utcnow()
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="test_modal")
    async def test_modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(modal=Questionnaire())
    
    @commands.command(name="the time has been come")
    async def ghost(self,ctx):
        await ctx.send("ghost time is comming...")
    
    @commands.command()
    async def credit(Self,ctx):
        embed = discord.Embed(title="WG server",description="Thanks to using Ghost World bot!",color=0x0000ff,url="https://discord.gg/WgMBCT4xxM")
        embed2 = discord.Embed(title="Noob server",description="Thanks to using Ghost World bot!",color=0xffff00,url="https://discord.gg/qFFbjEJS3h")
        embed3 = discord.Embed(title="Free_bat server",description="Thanks to using Ghost World bot!",color=0xa52a2a, url="https://discord.gg/dp5MvvUMXn")
        await ctx.send(embeds=[embed,embed2,embed3])
    


async def setup(bot): # this is called by Pycord to setup the cog
    await bot.add_cog(user(bot))