import discord
from discord.ext import commands
from discord.utils import get
import logging
#logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
#logger = logging.getLogger(__name__)

class TicketDCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def ticket_donate(self, ctx:commands.Context):
        """
        Sends a message with a 'Create Ticket' button.
        """
        view = CreateTicketView()
        view.timeout = None
        #await ctx.delete()
        await ctx.send("Click the button to create a ticket!", view=view)

    @ticket_donate.error
    async def error(self, ctx, error):
        await ctx.send(error)

class CreateTicketView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Add a button to the View
        #self.add_item(discord.ui.Button(label='Create Ticket'))

    @discord.ui.button(label='Create Donation Ticket',style=discord.ButtonStyle.blurple)
    async def create_ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Handles the 'Create Ticket' button click: creates a new ticket channel.
        """
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
        channel = await category.create_text_channel('ticket | donation', overwrites=overwrites)

        # Add a 'Close Ticket' button to the new channel
        view = CloseTicketView()
        view.timeout = None
        await channel.send(f"{interaction.user.mention} 후원문의를 눌르셧습니다.\n 관리자의 연락이 올때까지 기달리십시요.", view=view)

        # Respond to the button click
        await interaction.response.send_message(f"Created a new ticket: {channel.mention}!",ephemeral = True)

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
            await interaction.response.send_message(f"{interaction.user.mention} dude you are not ADMIN",ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketDCog(bot))
