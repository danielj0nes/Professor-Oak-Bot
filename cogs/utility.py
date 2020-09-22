import discord
from database.db import SQL
from discord.ext import commands
import asyncio


class Utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["cp", "prefix"])
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix):
        """Changes the command prefix of the bot for your server.
        **Example**: `!cp .`
        *Requires administrator permissions*."""
        await ctx.message.delete()
        sql = SQL()
        sql.update_prefix(ctx.guild.id, prefix)
        await ctx.send(f"The bot's command prefix has been changed to `{prefix}`.")



def setup(client):
    client.add_cog(Utility(client))
