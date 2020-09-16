import discord
from discord.ext import commands
from database.db import SQL


class Calculator(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def iv(self, ctx, attack: int, defence: int, hp: int):
        """Calculates the IV of a Pokemon given the attack, defence, and HP values found on the appraisal screen.
        **Example**: `!iv 15 14 13`"""
        if [False for i in (attack, defence, hp) if i < 0 or i > 15]:
            await ctx.author.send("One or more values are invalid. Attack, defence, and hp can be between 0 - 15.")
        else:
            await ctx.author.send(f"IV: {(attack + defence + hp) / 0.45}")


def setup(client):
    client.add_cog(Calculator(client))
