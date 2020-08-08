# gen.py
import discord, time, random
from discord.ext import commands
from discord import Member
import json


class Gen(commands.Cog):    
    
    with open('loot.json') as f:
        data = json.load(f)  
          
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("gen.py is active")
        print(data)

    @commands.command()
    async def hi(self, ctx):
        await ctx.send("this was sent from a cog lol")


def setup(bot):
    bot.add_cog(Gen(bot))
