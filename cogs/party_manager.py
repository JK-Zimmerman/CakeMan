'''
party_manager.py
As a party is a social function, party_manager is responsible with directly interfacing with users (via commands)
Last updated: 2024 12 17
'''
import discord
from cogs.modules.authenticate import Authenticator
from cogs.modules.leaderboard import Leaderboard_Manager
from cogs.modules.liege import Liege
from discord.ext import commands
import matplotlib.pyplot as plt

class PartyManager(commands.Cog, Leaderboard_Manager, Authenticator, Liege):
    def __init__(self, bot, liege = 317740007605534722, rcrdstoragefile:str = "authenticate.db",
                 ldrbrdstoragefile:str = "leaderboard.db", lstorage_file = 'liege.db'):
        self.bot = bot
        self.liege = liege

        Leaderboard_Manager.__init__(self, word = 'wish', plural = 'es', storagefile = ldrbrdstoragefile)
        Authenticator.__init__(self, storagefile = rcrdstoragefile)
        Liege.__init__(self, liege = liege, storagefile = lstorage_file)


    #authorization function
    def check_liege(ctx) -> bool:
        return ctx.cog.is_liege(ctx.author.id)
    
    #defining commands
    @commands.command()
    async def liege(self, ctx) -> None: #add liege, if none exists
        try:
            if not self.exists_liege() or self.is_liege(ctx.author.id):
                self.add_liege(ctx.author.id)
                await ctx.reply('My liege.', mention_author=False)
            else:
                await ctx.reply('Gargle my balls.', mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command()
    async def unliege(self, ctx) -> None: #remove liege
        try:
            if self.get_liege() == ctx.author.id:
                self.remove_liege()
                await ctx.reply('Farewell, my liege.', mention_author=False)
            else:
                await ctx.reply('Gargle my balls.', mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command()
    @commands.check(check_liege)
    async def manual_update(self, ctx, arg:str): # Manually adds one to records associated with name
        try:
            await ctx.reply(self.update(arg), mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command() 
    @commands.check(check_liege)
    async def manual_override(self, ctx, name:str, wish:int) -> None: #records associated with name are changed to wish
        try:
            await ctx.reply(self.override(name, wish), mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command()   
    @commands.check(check_liege)   
    async def reset(self, ctx) -> None: #leaderboard is wiped
        try:
            await ctx.reply(self.total_reset(), mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command()      
    async def push_ldr(self, ctx) -> None:
        try:
            await ctx.reply(self.ldr_quick_save(), mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command()      
    async def show(self, ctx): #print leader board
        try:
            await ctx.send(str(self))
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command()  
    @commands.check(check_liege)   
    async def reset_record(self, ctx) -> None: #wipe records of past birthdays
        try:
            await ctx.reply(self.complete_reset(), mention_author=True) 
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command()
    @commands.check(check_liege)
    async def delete_date(self, ctx, year:int, month:int, day:int) -> None: #deletes provided date (formatted like YYYY (M)M (D)D) from records of past birthdays
        try:
            await ctx.reply(self.deleteDate(year, month, day), mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command() #adds provided data to records of past birthdays
    @commands.check(check_liege)
    async def add_date(self, ctx, year:int, month:int, day:int) -> None:
        print(self.check_liege)
        try:
            await ctx.reply(self.addDate(year, month, day), mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)
    
    @commands.command()
    @commands.check(check_liege)
    async def add_dates(self, ctx, *args) -> None: #adds provided arbitrary number of dates (formatted like YYYY (M)M (D)D and separated by , ; or .)
        try:
            arguments = ''.join(args)
            if ';' in arguments:
                arguments = arguments.split(';')
            elif ',' in arguments:
                arguments = arguments.split(',')
            elif '.' in arguments:
                arguments = arguments.split('.')
            else:
                raise Exception('No valid separator.')
            
            for i in arguments:
                self.addDate(int(i[:4]), int(i[4:6]), int(i[6:8]))
            await ctx.reply('Completed.', mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command()
    async def push_dates(self, ctx) -> None:
        try:
            await ctx.reply( self.bot.record_quick_save(), mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)
    
    @commands.command()
    async def show_record(self, ctx) -> None: #shows birthday records
        try:
            await ctx.reply(Authenticator.__str__(self), mention_author=True)
        except:
            await ctx.reply('Error: Something fucked up', mention_author=True)

    @commands.command()
    async def graph(self,ctx) -> None: #give bar graph of current standings
        data = self.get_leaderboard()
        
        x = [await self.bot.fetch_user(int(point[0][2:-1])) for point in data]
        print(x)
        print(type(x[0]))
        for point in x:
            print(type(point.name))
            point = point.name
        print(x)
        #x = [point.name for point in data]
        y = [point[1] for point in data]

        plt.clf() 
        fig, ax = plt.subplots()
        ax.bar(x = list(range(len(x))), height = y)
        ax.set_xticks(list(range(len(x))), x, rotation=20)
        ax.set_ylabel('Wishes')
        ax.set_title('Current Standings')
        plt.subplots_adjust(bottom=0.19)
        plt.savefig(fname='plot')
        await ctx.reply(file=discord.File('plot.png'), mention_author=True)



async def setup(bot):
    await bot.add_cog(PartyManager(bot))