'''
main.py
Main is responsible for starting up bot and loading, unloading, reloading cogs.
Last updated: 2024 12 16
'''
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.presences = False
intents.dm_messages = True
intents.dm_reactions = True
intents.reactions = True
intents.messages = True
intents.message_content = True
intents.members = True

description = 'A bot to count who wished others a happy birthday the most.'
command_prefix = '!cake:'

bot = commands.Bot(command_prefix=command_prefix, description=description, intents = intents)

@bot.event
async def on_ready() -> None: #loads all cogs when ready to start
    for filename in os.listdir('.\\cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def load(ctx, extension:str): #load specified cog
    await bot.load_extension(f'cogs.{extension}')
    await ctx.reply('Loaded.', mention_author=True)

@bot.command()
async def unload(ctx, extension:str) -> None: #removes specified cog
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.reply('Unloaded.', mention_author=True)

@bot.command()
async def reload(ctx, extension:str): #reloads specified cog
    await bot.unload_extension(f'cogs.{extension}')
    await bot.load_extension(f'cogs.{extension}')
    await ctx.reply('Reloaded.', mention_author=True)

bot.run(token)