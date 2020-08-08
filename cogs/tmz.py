# tmz.py
import discord, time, random
from discord.ext import commands
from discord import Member
import json

from timezonefinder import TimezoneFinder
from datetime import datetime
from pytz import timezone, utc, country_timezones
import aiohttp


class TMZ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_timezone")
    async def get_timezone(self, ctx, ip):
        """
        returns a location's time zone offset from UTC in minutes
        """
        ip = str(ip)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.radar.io/v1/geocode/ip', params=ip) as r:
                expect = 'https://api.radar.io/v1/geocode/ip?ip'
                assert str(r.url) == expect
        print(await r.text())

        # with open("ip.json", mode="w") as f:
        #     json.dump(output, f, indent=4)

        # with open("ip.json", mode="r") as f:
        #     data = json.load(f)

        # lat = float(data["address"]["latitude"])
        # lng = float(data["address"]["longitude"])

        # today = datetime.now()
        # tf = TimezoneFinder()
        # tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
        # today_target = tz_target.localize(today)
        # today_utc = utc.localize(today)
        # await ctx.send("You are:", (today_utc - today_target).total_seconds() / 60, "away from UTC")


def setup(bot):
    bot.add_cog(TMZ(bot))
