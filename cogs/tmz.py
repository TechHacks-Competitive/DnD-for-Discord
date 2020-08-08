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


# with open("timezone.json") as f:
#     data = json.load(f)


# def write_json(data, filename='timezone.json'):
#     with open(filename, 'w') as f:
#         json.dump(data, f, indent=4)


class TMZ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nextgametime")
    async def nextgametime(self, ctx, ip):
        """
        returns the next optimal time to play the next session
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
                utc_offset = (today_utc - today_target).total_seconds() / 3600
                await ctx.send(f"You are: {utc_offset} hours away from UTC")


def setup(bot):
    bot.add_cog(TMZ(bot))
