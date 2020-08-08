import json
import os
import random

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="$")
TOKEN = os.environ.get("TOKEN")


# Registering an event
@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    servers = list(bot.guilds)
    server_num = len(servers)
    print(bot.user.id)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"over {server_num} servers || $help",
        )
    )


@bot.command()
async def roll(ctx: commands.Context, dice: str = "1d20"):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split("d"))
    except Exception:
        await ctx.send("Format has to be in NdN!")
        return

    results = [random.randint(1, limit) for _ in range(rolls)]

    result = ", ".join([str(x) for x in results])
    result = f"**{result}**"

    print(results)

    if len(results) > 1:
        result += f"\nSum: {sum(results)}"

    await ctx.send(result)


@bot.command()
async def echo(ctx: commands.Context, message: str):
    """Echos `message`"""
    await ctx.send(message)




for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(TOKEN)
