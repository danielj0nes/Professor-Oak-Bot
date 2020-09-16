import discord
from discord.ext import commands
import requests
from datetime import datetime


def get_stats(pokemon):
    """Parse json data to get the base stats and pokémon id number"""
    data_source = "https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-json-pokedex/master/output/pokemon.json"
    poke_data = requests.get(data_source).json()
    stats = []
    for mon in poke_data:
        try:
            if mon["name"] == pokemon.capitalize():
                for stat in mon["stats"].values():
                    stats.append(stat+15)  # Add 15 to each stat since we only care about 100 iv (potential to change)
                stats.append(str(mon["dex"]).zfill(3))
                return stats
        except TypeError:
            return False


class Calculator(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.multipliers = {15: 0.51739395, 20: 0.5974,
                            25: 0.667934, 30: 0.7317,
                            35: 0.76156384, 40: 0.7903}

    @commands.command()
    async def iv(self, ctx, attack: int, defence: int, hp: int):
        """Calculates the IV of a Pokemon given the attack, defence, and HP values found on the appraisal screen.
        **Example**: `!iv 15 14 13`"""
        await ctx.message.delete()
        if [False for i in (attack, defence, hp) if i < 0 or i > 15]:
            await ctx.author.send("One or more values are invalid. Attack, defence, and hp can be between 0 - 15.")
        else:
            await ctx.author.send(f"IV: {(attack + defence + hp) / 0.45}")

    @commands.command()
    async def best(self, ctx, pokemon, channel=""):
        """Calculates and displays 100 IV variants of a pokemon at a certain level.
        **Example**: `!best Rayquaza` or `!best Rayquaza public` (to display in the current channel)."""
        await ctx.message.delete()
        stats = get_stats(pokemon)
        if stats:
            icon = "https://static.wikia.nocookie.net/pokemongo_gamepedia_en/images/6/67/Button_poke_menu.png/"
            best_versions = discord.Embed(color=0xFF0000, timestamp=datetime.utcnow())
            best_versions.set_author(name=f"{pokemon.capitalize()} - #{stats[3]}",
                                     icon_url=icon)
            best_versions.add_field(name=f"100 IV variants of {pokemon.capitalize()}", value="\u200b", inline=False)
            best_versions.add_field(name="""Level        CP""", value="\u200b", inline=False)
            for level, multiplier in self.multipliers.items():
                best_versions.add_field(name=f"""{level}             {int((stats[0] * stats[1]**0.5 * stats[2]**0.5 * multiplier**2) // 10)}""",
                                        value="\u200b",
                                        inline=False)
            best_versions.set_thumbnail(url=f"https://images.gameinfo.io/pokemon/256/{stats[3]}-00.png")
            if channel.lower() == "public":
                await ctx.send(embed=best_versions)
            else:
                await ctx.message.author.send(embed=best_versions)


def setup(client):
    client.add_cog(Calculator(client))
