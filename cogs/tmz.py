# tmz.py
import discord, time, random
from discord.ext import commands
from discord import Member

from timezonefinder import TimezoneFinder
from datetime import datetime
from pytz import timezone, utc

class TMZ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="get_offset")
    async def get_offset(self,ctx,lat,lng):
        """
        returns a location's time zone offset from UTC in minutes.
        """
        lat = float(lat)
        lng = float(lng)1

        today = datetime.now()
        tf = TimezoneFinder()
        tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
        today_target = tz_target.localize(today)
        today_utc = utc.localize(today)
        await ctx.send( (today_utc - today_target).total_seconds() / 60 )



def setup(bot):
    bot.add_cog(TMZ(bot))
