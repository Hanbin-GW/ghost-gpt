import discord
from discord.ext import commands
import asyncio
import time
import logging

#logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
#logger = logging.getLogger(__name__)

log_channel_id_edit = 1093478970630082602
log_channel_id_delete = 1093477677773623397

LOG_CHANNELS_EDIT = {
        '879204407496028201': '1156651023952248852',
        '1069174895893827604': '1150054905097228359',
        '1156939299950973000': '1165636530048602203'
        
    # ... 여러 길드들 ...
    }
LOG_DELETE_CHANNELS = {
        '879204407496028201': '1150054808015872031',
        '1069174895893827604': '1156652048570396673',
        '1156939299950973000': '1165636530048602203'
}



class message(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    # 길드 ID를 키로하고 로그 채널 ID를 값으로하는 사전
    

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
    # 메세지 내용이 바뀌었는지 확인
        if before.content != after.content:
        # 메시지가 수정된 길드의 ID를 기반으로 로그 채널을 얻습니다.
            log_channel_id = LOG_CHANNELS_EDIT.get(str(before.guild.id))
            if log_channel_id:
                try:
                    log_channel_edit = self.bot.get_channel(int(log_channel_id))
                # 채널이 유효한지 확인
                    if log_channel_edit:
                        embed = discord.Embed(title="Message Edit Log",description=f"메시지가 {before.author.name}에 의해 수정되었습니다.\n전: {before.content} \n후: {after.content}",color=0xffa500)
                        await log_channel_edit.send(embed=embed)
                        embed.add_field(name="전",value=f"{before.content}")
                        embed.add_field(name='후',value=f"{after.content}")
                        #await log_channel_edit.send(f"Message edited by {before.author.name}: \n전: {before.content} \n후: {after.content}")
                    else:
                        print(f"Failed to get the log channel for guild ID: {before.guild.id}")
                except Exception as e:
                    print(f"Error accessing log channel for guild ID: {before.guild.id}. Error: {e}")
        else:
            print(f"No log channel found for guild ID: {before.guild.id}")
    
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        log_channel_id = LOG_DELETE_CHANNELS.get(str(message.guild.id))
        if log_channel_id:
            try:
                log_channel_edit = self.bot.get_channel(int(log_channel_id))
                # 채널이 유효한지 확인
                if log_channel_edit:
                    embed = discord.Embed(title=f"삭제됨", description=f"유저 : {message.author.mention} 채널 : {message.channel.mention}", color=0xFF0000)
                    embed.add_field(name="삭제된 내용", value=f"내용 : {message.content}", inline=False)
                    embed.set_footer(text=f"{message.guild.name} | {time}")
                    await log_channel_edit.send(embed=embed)
                else:
                        print(f"Failed to get the log channel for guild ID: {message.guild.id}")
            except Exception as e:
                print(f"Error accessing log channel for guild ID: {message.guild.id}. Error: {e}")
        else:
            print(f"No log channel found for guild ID: {message.guild.id}")
            
        # if not message.guild: return # DM Message
async def setup(bot): # this is called by Pycord to setup the cog
    await bot.add_cog(message(bot))

