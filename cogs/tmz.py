# tmz.py
import discord, time, random
from discord.ext import commands
from discord import Member

from timezonefinder import TimezoneFinder
from datetime import datetime
from pytz import timezone, utc, country_timezones


class TMZ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_offset")
    async def get_offset(self, ctx, lat, lng):
        """
        returns a location's time zone offset from UTC in minutes.
        """
        lat = float(lat)
        lng = float(lng)

        today = datetime.now()
        tf = TimezoneFinder()
        tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
        today_target = tz_target.localize(today)
        today_utc = utc.localize(today)
        await ctx.send((today_utc - today_target).total_seconds() / 60)

    @commands.command(name="get_")
    async def get_(self, ctx, lat, lng):
        """
        returns country code
        """
        timezone_country = {}
        for countrycode in country_timezones:
            timezones = country_timezones[countrycode]
            for timezon in timezones:
                timezone_country[timezone] = countrycode
                await ctx.send(countrycode)


def setup(bot):
    bot.add_cog(TMZ(bot))
