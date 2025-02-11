import discord
from discord.ext import commands
from discord import app_commands
from color_ansi import Color
import wavelink
class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        bot.loop.create_task(self.setup_hook())
    

    async def setup_hook(self):
        node: wavelink.Node = wavelink.Node(uri='lavalink.lexnet.cc', password='lexn3tl@val!nk',secure=True)
        await wavelink.NodePool.connect(client=self, nodes=[node])

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in {self.user} | {self.user.id}')

    @commands.command()
    async def play(self,ctx: commands.Context, *, search: str):
        """Simple play command."""

        if not ctx.voice_client:
            vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc = ctx.voice_client

        tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(search)
        if not tracks:
            await ctx.send(f'Sorry I could not find any songs with search: `{search}`')
            return

        track: wavelink.YouTubeTrack = tracks[0]
        await vc.play(track)


    @commands.command()
    async def disconnect(self,ctx: commands.Context):
        """Simple disconnect command.

        This command assumes there is a currently connected Player.
        """
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()


async def setup(bot):
    await bot.add_cog(Music(bot))