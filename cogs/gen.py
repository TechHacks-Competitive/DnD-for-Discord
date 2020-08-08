# gen.py
import discord, time, random
from discord.ext import commands
from discord import Member
import json

with open('loot.json') as f:
    data = json.load(f)  
    
weighted_tb = []

class Gen(commands.Cog):    
          
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("gen.py is active")
        loot_table = data["level_1"]["magic_tb"]
        for item,weight in loot_table:
            for _ in range(weight):
                weighted_tb.append(item)

    @commands.command()
    async def hi(self, ctx):
        await ctx.send("this was sent from a cog lol")
         
    @commands.command()
    async def loot(self, ctx, items=1):
        invn = ""
        for _ in range(items):
            invn += (random.choice(weighted_tb)) + '\n'
        await ctx.send('```'+invn+'```')


def setup(bot):
    bot.add_cog(Gen(bot))
