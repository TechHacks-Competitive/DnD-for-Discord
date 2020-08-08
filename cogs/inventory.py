import discord
from discord.ext import commands


class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="inventory")
    async def get_inventory(self, ctx: commands.Context):
        if ctx.author.id in inventory:
            inv = "\n".join([f"- {i}" for i in inventory[ctx.author.id]])

            await ctx.author.send(f"Your inventory is:\n{inv}")
        else:
            await ctx.author.send(f"You have no items in your inventory!")

        await ctx.message.add_reaction("✔️")

    @commands.command()
    async def addinv(self, ctx: commands.Context, item: str):
        if ctx.author.id not in inventory:
            inventory[ctx.author.id] = []

        inventory[ctx.author.id].append(item)

        await ctx.message.add_reaction("✔️")


def setup(bot):
    bot.add_cog(Inventory(bot))
