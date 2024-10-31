import discord
from discord.ext import commands

# Bot setup

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!',intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I am your new bot!")

# Run the bot
bot.run('MTMwMDc4MjU4ODU0MTE0NTExOQ.GDPjIW.99qteikt9ffcf9QP9wwrbcM74utgo7fDRoeR2o')  # Replace with your bot token
