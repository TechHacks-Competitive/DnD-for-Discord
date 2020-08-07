import discord
from discord.ext import commands
import random,os
from dotenv import load_dotenv
load_dotenv()


# client = discord.Client()
bot = commands.Bot(command_prefix='$')
TOKEN = os.environ.get('TOKEN')



# Registering an event
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    servers = list(bot.guilds)
    server_num = len(servers)
    print(bot.user.id)
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {server_num} servers || $help"))




@bot.command()
async def roll(ctx, dice: str):
    # Rolls a dice in NdN format.
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send("**"+str(result)+"**")


@bot.command()
async def echo(ctx, message: str):
    await ctx.send(message)


bot.run(TOKEN)
