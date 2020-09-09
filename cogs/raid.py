import discord
from discord.ext import commands
from datetime import datetime


class Raid(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def raid(self, ctx, pokemon, time, *gymname):
        await ctx.channel.purge(limit=1)
        thumbnail = f"https://img.pokemondb.net/artwork/{pokemon.lower()}.jpg"
        gym_url = "+".join(gymname)
        raid = discord.Embed(title=":house: Gym", url=f"https://www.google.com/maps/search/{gym_url}",
                             description=" ".join(gymname), color=0x32cd32, timestamp=datetime.utcnow())
        raid.set_author(name=f"Raid polled by {ctx.message.author.nick}")
        raid.set_thumbnail(url=thumbnail)
        raid.add_field(name=":alarm_clock: Start time", value=time)
        raid.add_field(name=":dragon_face: Pokémon / Difficulty", value=pokemon.capitalize())
        raid.set_footer(text=f"Thanks to {ctx.message.author.nick} for polling the raid. "
                             f"Please react to this message indicate your attendance")
        await ctx.send(embed=raid)
        await ctx.send("@here")


def setup(client):
    client.add_cog(Raid(client))
