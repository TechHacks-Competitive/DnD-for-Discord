# tmz.py
import json
import os
import random
import time
from datetime import datetime

import aiohttp
import discord
from discord import Member
from discord.ext import commands
from pytz import country_timezones, timezone, utc
from timezonefinder import TimezoneFinder


class TMZ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_timezone")
    async def get_timezone(self, ctx, ip):
        """
        returns a location's time zone offset from UTC in minutes
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.radar.io/v1/geocode/ip",
                params={"ip": ip},
                headers={"Authorization": os.environ.get("RADAR_TOKEN")},
            ) as r:
                r = await r.json()
                lat = r["address"]["latitude"]
                lng = r["address"]["longitude"]

                today = datetime.now()
                tf = TimezoneFinder()
                tz_target = timezone(tf.certain_timezone_at(lng=lng, lat=lat))
                today_target = tz_target.localize(today)
                today_utc = utc.localize(today)
                await ctx.send(
                    f"You are: {(today_utc - today_target).total_seconds() / 60} hours away from UTC"
                )


def setup(bot):
    bot.add_cog(TMZ(bot))
