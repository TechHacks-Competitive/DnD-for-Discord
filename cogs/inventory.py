import json
import os

import discord
<<<<<<< HEAD
from discord.ext import commands
import json
from discord import Member
=======
from discord.ext import commands, tasks
>>>>>>> b5d509affb3341915f0dbac4764b694ac54e1762


class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.inventory = {}
        self.old_inventory = {}

        if os.path.exists("inventory.json"):
            with open("inventory.json") as f:
                self.inventory = json.load(f)
                self.old_inventory = self.inventory

    @tasks.loop(minutes=5)
    async def save_inventory():
        if self.inventory != self.old_inventory:
            with open("inventory.json", mode="w") as f:
                json.dump(self.inventory, f)

            self.old_inventory = self.inventory

    @commands.command(name="inventory")
    async def get_inventory(self, ctx: commands.Context):
<<<<<<< HEAD
        if ctx.author.id in inventory:
            inv = "\n".join([f"- {items}" for items in inventory[ctx.author.id]])
=======
        if ctx.author.id in self.inventory:
            inv = "\n".join([f"- {i}" for i in self.inventory[ctx.author.id]])
>>>>>>> b5d509affb3341915f0dbac4764b694ac54e1762

            await ctx.author.send(f"Your inventory is:\n{inv}")
        else:
            await ctx.author.send(f"You have no items in your inventory!")

        await ctx.message.add_reaction("✔️")

    @commands.command()
    async def addinv(self, ctx: commands.Context, item: str):
        if ctx.author.id not in self.inventory:
            self.inventory[ctx.author.id] = []

        self.inventory[ctx.author.id].append(item)

        await ctx.message.add_reaction("✔️")


def setup(bot):
    bot.add_cog(Inventory(bot))
