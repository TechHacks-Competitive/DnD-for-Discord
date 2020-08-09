# tmz.py
import json
import os
import random
import time
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands, tasks
from pytz import country_timezones, timezone, utc
from timezonefinder import TimezoneFinder


class TMZ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.old_tz = {}
        self.tz = {}

        if os.path.exists("timezone.json"):
            with open("timezone.json") as f:
                self.tz = json.load(f)

    @tasks.loop(minutes=5)
    async def save_tz():
        if self.tz != self.old_tz:
            with open("timezone.json", mode="w") as f:
                json.dump(self.tz, f)

            self.old_tz = self.tz

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
            self.tz[ctx.author.id] = int(utc_offset)
            with open("timezone.json", mode="w") as f:
                json.dump(self.tz, f)
        elif ctx.author.id in self.tz:
            # return the timezone from the json file
            authortimezone = self.tz[ctx.author.id]
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
        # 1. [X] get list of timezones of each player from timezone.json
        # 2. create absolute UTC array of 0 = dark hours and !0 = wake hours
        # 3. create more timezone equivalent arrays via subtracting/adding each value by the UTC offset #
        # FORMAT:
        # [1,   2,  3,  4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] UTC(0)
        # [21, 22, 23, 24, 1, 2, 3, 4, 5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] EST(-4)
        # etc
        # 4. Loop through the same columns of these arrays and return the column with the most amount of non-zero numbers
        UTC = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
        ]
        UTC = [
            0 if hour > 22 or hour < 7 else hour for hour in UTC
        ]  # Replace sleeping hours with 0s

        equiv = {}

        for member in self.tz.keys():
            equiv[member] = []

            for x in [x + self.tz[member] for x in UTC]:
                if x == 1:
                    equiv[member].append(0)
                else:
                    equiv[member].append(x)

        good = {}

        for member in self.tz.keys():
            for idx, eq in enumerate(equiv[member]):
                if eq != 0:
                    if idx not in good:
                        good[idx] = 1
                    else:
                        good[idx] += 1

        good = sorted(good.items(), key=lambda x: x[1], reverse=True)

        el = {}

        for x in good:
            h = x[0]

            el[h] = 0 if h <= 15 and h >= 6 else 1

        print(good)

        early = []
        for x in good:
            if el[x[0]] == 0:
                early.append(x[0])

        late = []
        for x in good:
            if el[x[0]] == 1:
                late.append(x[0])

        early = early[:3]
        late = late[:3]

        message = "Early times:\n"

        for x in early:
            message += f"- Hour {x}\n"

        message += "\nLate Times:\n"

        for x in late:
            message += f"- Hour {x}\n"

        await ctx.send(message)


def setup(bot):
    bot.add_cog(TMZ(bot))
