# gen.py
import discord, time, random
from discord.ext import commands
from discord import Member
import json

with open("loot.json") as f:
    data = json.load(f)

weighted_tb = []
def write_json(data, filename='loot.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 


class Gen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("gen.py is active")
        loot_table = data["level_1"]["magic_tb"]
        cust_loot_table = data["level_1"]["dm_"]["discriminator"]
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
        
    @commands.command()
    async def add_loot(self, ctx,*,item):
        nums = ctx.author.discriminator
        if nums in data["level_1"]["dm_"]["discriminator"]:
            data["level_1"]["dm_"]["discriminator"][nums].append(item)
        else:
            data["level_1"]["dm_"]["discriminator"][nums] = [item]

        write_json(data)
        await ctx.send("added!")
     
    @commands.command()
    async def cust_loot(self, ctx, nums: Member=0):
        if nums:
            nums = nums.discriminator
        else:
            nums = ctx.author.discriminator
        invn = ""
        for cust_itm in data["level_1"]["dm_"]["discriminator"][nums]:
            invn += cust_itm + '\n'
        await ctx.send('```'+invn+'```')



def setup(bot):
    bot.add_cog(Gen(bot))
