import discord
from discord.ext import commands
from datetime import datetime
from etc.poke_dict import poke_dict


class Pokedex(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["pd", "Pd", "Pokedex", "dex"])
    async def pokedex(self, ctx, pokemon, channel=""):
        """Look up a Pokemon by name to return information such as the different moves and max cp.
        **Example**: `!pd Pikachu` or `!pd Pikachu public` (to display in the current channel)."""
        pokemon = pokemon.capitalize()
        try:
            poke_details = poke_dict[pokemon]
            dex_icon = "https://static.wikia.nocookie.net/pokemongo_gamepedia_en/images/6/67/Button_poke_menu.png/"
            thumbnail = f"https://images.gameinfo.io/pokemon/256/{poke_details['id_no'].zfill(3)}-00.png"
            pokedex_entry = discord.Embed(color=0xFF0000, timestamp=datetime.utcnow())
            pokedex_entry.set_author(name=f"{pokemon} - #{poke_details['id_no']}", icon_url=dex_icon)
            pokedex_entry.add_field(name="Max CP", value=poke_details['maxCP'], inline=False)
            pokedex_entry.add_field(name="Type(s)", value=", ".join(poke_details['types']), inline=False)
            pokedex_entry.add_field(name="Charge moves", value=", ".join(poke_details['charged_moves']), inline=False)
            pokedex_entry.add_field(name="Fast moves", value=", ".join(poke_details['fast_moves']), inline=False)
            pokedex_entry.set_thumbnail(url=thumbnail)
            if channel.lower() == "public":
                await ctx.send(embed=pokedex_entry)
            else:
                await ctx.message.author.send(embed=pokedex_entry)
        except KeyError:
            await ctx.message.author.send(f"'{pokemon}' is not a valid Pokémon or is not yet recognised")


def setup(client):
    client.add_cog(Pokedex(client))
