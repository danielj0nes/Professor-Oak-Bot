import discord
from discord.ext import commands
from datetime import datetime
from etc.poke_dict import poke_dict


class Raiding(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Raid"])
    @commands.has_permissions(mention_everyone=True)
    async def raid(self, ctx, pokemon, time, *gymname):
        """Posts a Raid announcement to the current channel.
        **Example**: `!raid Charizard 13:37 buckingham palace`
        *Requires the user to have the 'mention everyone' permission since @here will be tagged*."""
        pokemon = pokemon.capitalize()
        try:
            pokemon_id = poke_dict[pokemon]['id_no']
            thumbnail = f"https://images.gameinfo.io/pokemon/256/{pokemon_id.zfill(3)}-00.png"
        except KeyError:
            thumbnail = "https://www.spriters-resource.com/resources/sheets/90/93321.png?updated=1498128601"

        raid = discord.Embed(
            title=":house: Gym", url=f"https://www.google.com/maps/search/{'+'.join(gymname)}",
            description=" ".join(gymname), color=0x32cd32, timestamp=datetime.utcnow())
        raid.set_author(name=f"Raid polled by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        raid.set_thumbnail(url=thumbnail)
        raid.add_field(name=":alarm_clock: Start time", value=time)
        raid.add_field(name=":dragon_face: Pokémon / Difficulty", value=pokemon)
        raid.set_footer(text=f"Thanks to {ctx.message.author} for polling the Raid. "
                             f"Please react to this message to indicate your attendance.")
        msg = await ctx.send(embed=raid)
        await msg.add_reaction("🤚")
        await ctx.send("@here")

    @raid.error
    async def raid_error_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.author.send("The 'raid' command requires you to have the "
                                  "'mention everyone' permission, which you do not have.")

    @commands.command(aliases=["exraid", "Exraid", "EXRaid"])
    async def ex_raid(self, ctx, pokemon, time, *gym_name):
        """Posts an EX Raid announcement to the current channel.
        **Example**: `!exraid Deoxys 14:20 times square`"""
        pokemon = pokemon.capitalize()
        try:
            pokemon_id = poke_dict[pokemon]['id_no']
            thumbnail = f"https://images.gameinfo.io/pokemon/256/{pokemon_id.zfill(3)}-00.png"
        except KeyError:
            thumbnail = "https://www.spriters-resource.com/resources/sheets/90/93321.png?updated=1498128601"

        ex_raid_embed = discord.Embed(
            title=":house: Gym", url=f"https://www.google.com/maps/search/{'+'.join(gym_name)}",
            description=" ".join(gym_name), color=0x8B008B, timestamp=datetime.utcnow())
        ex_raid_embed.set_author(name=f"EX Raid polled by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        ex_raid_embed.set_thumbnail(url=thumbnail)
        ex_raid_embed.add_field(name=":alarm_clock: Start time", value=time)
        ex_raid_embed.add_field(name=":dragon_face: Pokémon / Difficulty", value=pokemon)
        ex_raid_embed.set_footer(text=f"Thanks to {ctx.message.author} for polling the EX Raid. "
                               f"Please react to this message to indicate your attendance.")
        msg = await ctx.send(embed=ex_raid_embed)
        await msg.add_reaction("🤚")


def setup(client):
    client.add_cog(Raiding(client))
