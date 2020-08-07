import json
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


inventory = {}
old_inventory = {}

if os.path.exists("inventory.json"):
    with open("inventory.json") as f:
        inventory = json.load(f)
        old_inventory = inventory


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


@tasks.loop(minutes=5)
async def save_inventory():
    global old_inventory

    if inventory != old_inventory:
        with open("inventory.json", mode="w") as f:
            json.dump(inventory, f)

        old_inventory = inventory


@bot.command()
async def roll(ctx: commands.Context, dice: str = "1d20"):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split("d"))
    except Exception:
        await ctx.send("Format has to be in NdN!")
        return

    result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send("**" + str(result) + "**")


@bot.command()
async def echo(ctx: commands.Context, message: str):
    """Echos `message`"""
    await ctx.send(message)


@bot.command()
async def getinv(ctx: commands.Context):
    await ctx.send("```\n" + inventory.__str__() + "\n```")


@bot.command()
async def addinv(ctx: commands.Context, item: str):
    if ctx.author.id not in inventory:
        inventory[ctx.author.id] = []
    inventory[ctx.author.id].append(item)
    await ctx.send("added!")


bot.run(TOKEN)
