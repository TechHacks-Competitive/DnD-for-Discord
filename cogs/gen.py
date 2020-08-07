# gen.py
import discord, time, random
from discord.ext import commands
from discord import Member


class Gen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("gen.py is active")

    @commands.command()
    async def hi(self, ctx):
        await ctx.send("this was sent from a cog lol")


def setup(bot):
    bot.add_cog(Gen(bot))
