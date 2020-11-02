import discord
from database.db import SQL
from discord.ext import commands
import random


class Game(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.starter_pokemon = ["Squirtle", "Charmander", "Bulbasaur", "Pikachu", "Chikorita", "Totodile", "Cyndaquil",
                                "Torchic", "Mudkip", "Treecko", "Turtwig", "Chimchar", "Piplup"]
        self.sql = SQL()

    @commands.command()
    async def start(self, ctx):
        """In progress..."""
        await ctx.message.delete()
        starter = random.choice(self.starter_pokemon)
        await ctx.send(f"You have been assigned `{starter}` as your starting Pokémon!")


def setup(client):
    client.add_cog(Game(client))
