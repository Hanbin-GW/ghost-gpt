import traceback
import discord
from discord.ext import commands
from discord.utils import get

name = " "
ID = " "
descriptions = " "

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Add a button to the View
        self.add_item(discord.ui.Button(label='Close Ticket'))

    @discord.ui.button(label='Close Ticket',style=discord.ButtonStyle.red)
    async def close_ticket_button(self, interaction: discord.Interaction,  button: discord.ui.Button):
        """
        Handles the 'Close Ticket' button click: deletes the ticket channel.
        """
        if interaction.user.guild_permissions.administrator:

            channel = interaction.channel

        # Delete the ticket channel
            await channel.delete()
        # Respond to the button click
            await interaction.response.send_message('The ticket was closed!')
            await interaction.user.send("the ticket was closed thaks to support")
        else:
            await interaction.user.send(f"{interaction.user.mention} dude you are not ADMIN")

class TicketManager:
    def __init__(self):
        self.tickets = []

    def create_ticket(self, user_name, steam_id, description):
        # 티켓 생성 로직
        self.tickets.append({
            "user_name": user_name,
            "steam_id": steam_id,
            "description": description
        })
        print("티켓 생성 완료!")


class Modal (discord.ui.Modal, title="Apply ban"):
    
    def __init__(self, on_submit_callback):
        super().__init__()
        self.on_submit_callback = on_submit_callback

    name_2 = discord.ui.TextInput(
        label="이름",
        placeholder='Your name here...',
        required=True
    )
    Steam_ID = discord.ui.TextInput(
        label="스팀ID",
        placeholder="당신의 Steam Id 를 주시면됩니다.",
        required=True,
    )
    explain = discord.ui.TextInput(
        label='당시 상황을 설명하십시요...',
        style=discord.TextStyle.long,
        placeholder='당시 상황을 설명하십시요...',
        required=True,
        max_length=300,
    )
    async def on_submit(self, interaction: discord.Interaction):
        user_name = self.name_2.value
        steam_id = self.Steam_ID.value
        description = self.explain.value
        await self.on_submit_callback(interaction, user_name, steam_id, description)
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)


class NewTicket(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="ticket2")
    @commands.is_owner()
    async def new_ticket(self, ctx : commands.Context):
        view = CreateTicketView()
        view.timeout = None
        await ctx.send("click the ticket" , view=view)

class CreateTicketView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Add a button to the View
        #self.add_item(discord.ui.Button(label='Create Ticket'))

    @discord.ui.button(label='Create Ticket',style=discord.ButtonStyle.green)
    async def create_ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Handles the 'Create Ticket' button click: creates a new ticket channel.
        """
        modal = Modal()
        await interaction.response.send_modal(modal)
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }
        category = discord.utils.get(guild.categories, name='Tickets')

        # If the 'Tickets' category does not exist, create it
        if category is None:
            category = await guild.create_category('Tickets')

        # Create a new ticket channel in the 'Tickets' category
        channel = await category.create_text_channel('ticket', overwrites=overwrites)

        # Add a 'Close Ticket' button to the new channel
        view = CloseTicketView()
        view.timeout = None
        await channel.send(f"New ticket created by {interaction.user.mention}! Click the button to close the ticket.", view=view)
        await channel.send(f"유저 : {name}\nSTEAM ID : {ID}\n설명 : {descriptions}")
        # Respond to the button click
        await interaction.response.send_message(f"Created a new ticket: {channel.mention}!",ephemeral = True)


async def setup(bot):
    await bot.add_cog(NewTicket(bot=bot))