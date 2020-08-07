import os
import random

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

# client = discord.Client()
bot = commands.Bot(command_prefix="$")
TOKEN = os.environ.get("TOKEN")


async def update_status():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"over {len(bot.guilds)} servers || $help",
        )
    )


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    await update_status()


@tasks.loop(minutes=10)
async def update_status_loop():
    await update_status()


@bot.command()
async def roll(ctx, dice: str = "1d20"):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split("d"))
    except:
        await ctx.send("Format has to be in NdN!")
        return

    result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command()
async def echo(ctx, message: str):
    """Echos `message`"""
    await ctx.send(message)


bot.run(TOKEN)
