import os
import discord
from discord import app_commands
from discord.ext import commands

folder_path = "bug_report"

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.TextInput(label="What is bot name??"))
        self.add_item(discord.ui.TextInput(label="세부사항"))

    async def callback(self, interaction: discord.Integration):
        nickname = interaction.user.name
        filename = f"{nickname}_bug_report.txt"
        file_path = os.path.join(folder_path, filename)
        bot_name = self.children[0].value
        des = self.children[1].value
        with open(file_path, 'w') as file_obj:
            file_obj.write(f"{nickname} is reporting {bot_name} 's error'.\ndescription -> {des}")
        await interaction.response.send_message("오류신고가 완료되었습니다!!")

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("운영체제", os.name)

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    @commands.command()
    async def bug_report(self, interaction : discord.Interaction):
        """Shows an example of a modal dialog being invoked from a slash command."""
        modal = MyModal(title="Bug Report [GW]")
        await interaction.response.send_modal(modal)

async def setup(bot):
    await bot.add_cog(Report(bot))