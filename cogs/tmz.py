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

bot = commands.Bot(command_prefix="$")


class TMZ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.tz = {}

        if os.path.exists("timezone.json"):
            with open("timezone.json") as f:
                self.tz = json.load(f)

    @commands.command(name="get_timezone")
    async def get_timezone(self, ctx, ip):
        """
        returns your timezone relative to UTC
        """
        if ctx.author.id not in self.tz:
            # Get GMT offset and store the offset in a json object
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
                    await ctx.author.send(f"You are: {utc_offset} hours from UTC")
            # Store UTC offset
            self.tz[ctx.author.id] = []
            self.tz[ctx.author.id].append(utc_offset)
            with open("timezone.json", mode="w") as f:
                json.dump(self.tz, f, indent=4)
        elif ctx.author.id in self.tz:
            # return the timezone from the json file
            authortimezone = self.tz[ctx.author.id][0]
            if authortimezone < 0:
                await ctx.author.send(f"Your timezone: (UTC{authortimezone})")
            elif authortimezone >= 0:
                await ctx.author.send(f"Your timezone: (UTC+{authortimezone})")
        await ctx.message.delete()

    @commands.command(name="nextgametime")
    async def nextgametime(self, ctx):
        """
        returns the best time to play the next game
        """
        # 1. get list of timezones of each player from timezone.json
        # 2. create absolute UTC array of 0 = dark hours and !0 = wake hours
        # 3. create more timezone equivalent arrays via subtracting each value by the UTC offset #
        # [1,   2   3,  4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] UTC(0)
        # [21, 22, 23, 24, 1, 2, 3, 4, 5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] EST(-4)
        # [0,   0   0,  0, 0, 0, 0, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,  0,  0] GMT(1)
        # etc
        # 4. Loop through the same columns of these arrays and return the column with the most amount of non-zero numbers
        playerstimezones = [timezones for timezones in self.tz]
        print(playerstimezones)


def setup(bot):
    bot.add_cog(TMZ(bot))
