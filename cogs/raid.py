import discord
from discord.ext import commands
from datetime import datetime


class Raiding(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(mention_everyone=True)
    async def raid(self, ctx, pokemon, time, *gymname):
        """Posts a Raid announcement to the current channel. **Example**: `!raid Charizard 13:37 buckingham palace`
        Requires the user to have the 'mention everyone' permission since @here will be tagged."""
        await ctx.message.delete()
        thumbnail = f"https://img.pokemondb.net/artwork/{pokemon.lower()}.jpg"
        gym_url = "+".join(gymname)
        raid = discord.Embed(
            title=":house: Gym", url=f"https://www.google.com/maps/search/{gym_url}",
            description=" ".join(gymname), color=0x32cd32, timestamp=datetime.utcnow())
        raid.set_author(name=f"Raid polled by {ctx.message.author.nick}")
        raid.set_thumbnail(url=thumbnail)
        raid.add_field(name=":alarm_clock: Start time", value=time)
        raid.add_field(name=":dragon_face: Pokémon / Difficulty", value=pokemon.capitalize())
        raid.set_footer(text=f"Thanks to {ctx.message.author.nick} for polling the Raid. "
                             f"Please react to this message indicate your attendance")
        msg = await ctx.send(embed=raid)
        await msg.add_reaction("🤚")
        await ctx.send("@here")

    @raid.error
    async def raid_error_handler(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingPermissions):
            await ctx.author.send("The 'raid' command requires you to have the "
                                  "'mention everyone' permission, which you do not have.")

    @commands.command()
    async def exraid(self, ctx, pokemon, time, *gymname):
        """Posts an EX Raid announcement to the current channel. **Example**: `!exraid Deoxys 14:20 times square`"""
        await ctx.message.delete()
        thumbnail = f"https://img.pokemondb.net/artwork/{pokemon.lower()}.jpg"
        gym_url = "+".join(gymname)
        exraid = discord.Embed(
            title=":house: Gym", url=f"https://www.google.com/maps/search/{gym_url}",
            description=" ".join(gymname), color=0x8B008B, timestamp=datetime.utcnow())
        exraid.set_author(name=f"EX Raid polled by {ctx.message.author.nick}")
        exraid.set_thumbnail(url=thumbnail)
        exraid.add_field(name=":alarm_clock: Start time", value=time)
        exraid.add_field(name=":dragon_face: Pokémon / Difficulty", value=pokemon.capitalize())
        exraid.set_footer(text=f"Thanks to {ctx.message.author.nick} for polling the EX Raid. "
                               f"Please react to this message indicate your attendance")
        msg = await ctx.send(embed=exraid)
        await msg.add_reaction("🤚")


def setup(client):
    client.add_cog(Raiding(client))
