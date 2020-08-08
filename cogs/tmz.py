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
                long = r["address"]["longitude"]

                await ctx.send(f"[{lat}, {long}]")


def setup(bot):
    bot.add_cog(TMZ(bot))
