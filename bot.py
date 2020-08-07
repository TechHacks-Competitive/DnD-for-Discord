import json
import os
import random

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

# client = discord.Client()
bot = commands.Bot(command_prefix="$")
TOKEN = os.environ.get("TOKEN")

inventory = {}
old_inventory = {}

if os.path.exists("inventory.json"):
    with open("inventory.json") as f:
        inventory = json.load(f)
        old_inventory = inventory


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
    except:
        await ctx.send("Format has to be in NdN!")
        return

    result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


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
