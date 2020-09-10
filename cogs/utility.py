import discord
from database.db import SQL
from discord.ext import commands
import asyncio


class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def change_prefix(self, ctx, prefix):
        """Changes the command prefix of the bot for your server"""
        sql = SQL()
        sql.update_prefix(ctx.guild.id, prefix)
        msg = await ctx.send(f"The bot's command prefix has been changed to '{prefix}'.")
        await asyncio.sleep(2)
        await msg.delete()


def setup(client):
    client.add_cog(Utility(client))
