import discord
from discord.ext import commands
import requests
from datetime import datetime


def poke_parser(pokemon):
    """Parse the pokemon go pokedex json data graciously provided by https://github.com/pokemongo-dev-contrib/"""
    id_cp, types, charged_moves, fast_moves = ([] for i in range(4))
    data_source = "https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-json-pokedex/master/output/pokemon.json"
    poke_data = requests.get(data_source).json()
    for mon in poke_data:
        try:
            if mon["name"] == pokemon.capitalize():
                id_cp.append(str(mon["dex"]).zfill(3))
                id_cp.append(mon["maxCP"])
                for poke_type in mon["types"]:
                    types.append(poke_type["name"])
                for charged_move in mon["cinematicMoves"]:
                    charged_moves.append(charged_move["name"])
                for fast_move in mon["quickMoves"]:
                    fast_moves.append(fast_move["name"])
                return [id_cp, types, charged_moves, fast_moves]
        except TypeError:
            return False


class Pokedex(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["pd", "Pd", "Pokedex", "dex"])
    async def pokedex(self, ctx, pokemon, channel=""):
        """Look up a pokémon by name to return information such as the different moves and max cp.
        **Example**: `!pd Pikachu` or `!pd Pikachu public` (to display in the current channel)."""
        await ctx.message.delete()
        data = poke_parser(pokemon)
        if data:
            pokedex_entry = discord.Embed(color=0xFF0000, timestamp=datetime.utcnow())
            pokedex_entry.set_author(name=f"{pokemon.capitalize()} - #{data[0][0]}",
                                     icon_url="https://static.wikia.nocookie.net/pokemongo_gamepedia_en/images/6/67/Button_poke_menu.png/")
            pokedex_entry.add_field(name="Max CP", value=data[0][1], inline=False)
            pokedex_entry.add_field(name="Type(s)", value=", ".join(data[1]), inline=False)
            pokedex_entry.add_field(name="Charge moves", value=", ".join(data[2]), inline=False)
            pokedex_entry.add_field(name="Fast moves", value=", ".join(data[3]), inline=False)
            pokedex_entry.set_thumbnail(url=f"https://images.gameinfo.io/pokemon/256/{data[0][0]}-00.png")
            if channel.lower() == "public":
                await ctx.send(embed=pokedex_entry)
            else:
                await ctx.message.author.send(embed=pokedex_entry)
        else:
            await ctx.message.author.send(f"'{pokemon}' is not a valid Pokémon or is not yet recognised")


def setup(client):
    client.add_cog(Pokedex(client))
