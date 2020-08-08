# gen.py
import discord, time, random
from discord.ext import commands
from discord import Member
from discord.utils import get
import json

# TODO: ADD WEIGHTS TO CUSTOM ITEMS TOO

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
        for item,weight in loot_table:
            for _ in range(weight):
                weighted_tb.append(item)



    @commands.command()
    async def loot(self, ctx, items=1):
        invn = ""
        cust_w_tb = weighted_tb.copy()
        
        role = get(ctx.guild.roles, name="DM")
        for dm in role.members:
            DM = dm
        cust_loot_table = data["level_1"]["dm_"]["discriminator"][str(dm.id)]
        for i in cust_loot_table:
            cust_w_tb.append(i)
            
        for _ in range(items):
            invn += (random.choice(cust_w_tb)) + '\n'
        await ctx.send('```'+invn+'```')
        
    @commands.command()
    async def add_loot(self, ctx,*,item):
        nums = ctx.author.id
        nums = str(nums)
        if nums in data["level_1"]["dm_"]["discriminator"]:
            data["level_1"]["dm_"]["discriminator"][str(nums)].append(item)
        else:
            data["level_1"]["dm_"]["discriminator"][str(nums)] = [item]

        write_json(data)
        await ctx.send("added!")
     
    @commands.command()
    async def del_loot(self, ctx,*,item):
        nums = ctx.author.id
        nums=str(nums)
        if nums in data["level_1"]["dm_"]["discriminator"]:
            data["level_1"]["dm_"]["discriminator"][nums].remove(item)
            await ctx.send("removed!")
        else:
            await ctx.send('lol that isn\'t in your custom loot table')
        write_json(data)
     
    @commands.command()
    async def cust_loot(self, ctx, nums: Member=0):
        try:
            if nums:
                nums = nums.id
            else:
                nums = ctx.author.id
            nums=str(nums)
                
            invn = '\n'.join(data["level_1"]["dm_"]["discriminator"][str(nums)])
            #print(invn)
            invn = f'\n```\n{invn}\n```\n'
            
            await ctx.send(invn)
        except KeyError:
            await ctx.send("no custom loot detected")



def setup(bot):
    bot.add_cog(Gen(bot))