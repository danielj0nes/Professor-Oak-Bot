"""danielj"""

import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import sqlite3
from datetime import datetime

# https://discordapp.com/oauth2/authorize?client_id=753011266187952288&scope=bot&permissions=8

def read_token():
    with open("token.txt", "r") as f:
        token = f.readlines()
        return token[0].strip()


bot = commands.Bot(command_prefix="!")
tkn = read_token()


@bot.command()
async def t(ctx):
    pass

bot.run(tkn)
