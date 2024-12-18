'''
cake_manager.py
Like a cake is the heart of a birthday, CakeManager is the heart of maintaining CakeMan. It is responsible for actually counting bithdays, as well as
related functionalities like aunthenticating birthdays.
Last updated: 2024 12 16
'''
import discord 
import regex as re
from cogs.modules.authenticate import Authenticator
from datetime import datetime
from discord.ext import commands
from cogs.modules.leaderboard import Leaderboard_Manager
from cogs.modules.liege import Liege
from zoneinfo import ZoneInfo


class CakeManager(commands.Cog, Leaderboard_Manager, Authenticator, Liege):
    def __init__(self, bot, liege = 317740007605534722, timezone:str = 'America/Los_Angeles', rcrdstoragefile:str = ".\\cogs\\modules\\authenticate.db",
                 ldrbrdstoragefile:str = ".\\cogs\\modules\\leaderboard.db", lstorage_file = '.\\cogs\\modules\\liege.db'):
        self.bot = bot
        self.timezone = ZoneInfo(timezone)

        Leaderboard_Manager.__init__(self, word = 'wish', plural = 'es', storagefile = ldrbrdstoragefile)
        Authenticator.__init__(self, storagefile = rcrdstoragefile)
        Liege.__init__(self, liege = liege, storagefile = lstorage_file)
        
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message) -> None: #checking all messaging for valid birhtday wishes, updates both databases when necessary
        #checks each message for birthday wishes, and authenticates if one is found
        if message.author == self.bot.user: # no infinite self reply
            return 
        
        if re.search('happy birthday', message.content.lower()):
            today = datetime.now(self.timezone).strftime(f'%Y-%m-%d')
            today = [int(i) for i in today.split('-')]
            if self.authenticateToday(today[0], today[1], today[2]): #checks if there is a record of someone else giving birthday wishes today
                if self.authenticateAllTime(today[1], today[2]): #check if theres a record of this being a birthday in past years (in case of late wishes, or other edge case)
                    self.addDate(today[0], today[1], today[2]) #if record exists, add it. Below logic accounts for Member and User cases. I don't understand when each happens, so just in case
                    if type(message.author) == discord.Member: 
                        self.update(message.author.name)
                    else:
                        self.update(message.author)
                else:  #if there is no record of this being a birthday, get approval
                    if not self.exists_liege() or await self.get_approval(message): #either there is no liege, or approval is attained from liege
                        self.addDate(today[0], today[1], today[2])
                        if type(message.author) == discord.Member:
                            self.update(message.author.name)
                        else:
                            self.update(message.author)
                    
    async def get_approval(self, message: discord.Message, timeout = None) -> bool: #seeks approval from liege, returns true if given 
        # gets approval from liege for message that can't be verified via dm reaction
        try:
            user = await self.bot.fetch_user(self.get_liege())
            approval_request = await user.send(f'Approval Request: "{message.content}" from {message.author.name} in {message.channel}') 

            await approval_request.add_reaction('👍')
            await approval_request.add_reaction('👎')
            reaction, user = await self.bot.wait_for("reaction_add", timeout=timeout)   

            if reaction.emoji == '👍':
                return True
            else:
                return False       
        except:
            return False
    
async def setup(bot):
    await bot.add_cog(CakeManager(bot))
