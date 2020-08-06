import discord
from discord.ext import commands
import random

# client = discord.Client()
bot = commands.Bot(command_prefix='$')


# Registering an event
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)


@bot.command()
async def roll(ctx, dice: str):
    # Rolls a dice in NdN format.
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command()
async def echo(ctx, message: str):
    await ctx.send(message)


bot.run('NzQxMDM4NjcyMzQ1OTU2NDE0.XyxwCw.c4EpKZs1WBo7FRuFAaIRUoLMKHo')
