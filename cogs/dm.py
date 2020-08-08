import discord
from discord.ext import commands
from discord import Member
from discord.utils import get
red = discord.Color.red()

class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("DM.py is active")

    @commands.command()
    async def dm(self, ctx, new_DM: Member=None):
        if not (new_DM):
            new_DM = ctx.author
        role = get(ctx.guild.roles, name="DM")
        if role:
            await role.delete()
        await ctx.guild.create_role(name="DM", color=red)
        await new_DM.add_roles(get(ctx.guild.roles, name="DM"))


def setup(bot):
    bot.add_cog(DM(bot))
