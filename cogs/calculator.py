import discord
from discord.ext import commands
import requests
from datetime import datetime
from etc.poke_dict import poke_dict


class Calculator(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.multipliers = {40: 0.7903, 35: 0.76156384,
                            30: 0.7317, 25: 0.667934,
                            20: 0.5974, 15: 0.51739395}

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
        """Calculates and displays 100 IV variants of a Pokemon at a certain level.
        **Example**: `!best Rayquaza` or `!best Rayquaza public` (to display in the current channel)."""
        await ctx.message.delete()
        try:
            pokemon = pokemon.capitalize()
            stats = [i + 15 for i in poke_dict[pokemon]["base_stats"]]  # 15 is for perfect IV, considering user variables
            dex_no = poke_dict[pokemon]["id_no"]
            icon = "https://static.wikia.nocookie.net/pokemongo_gamepedia_en/images/6/67/Button_poke_menu.png/"
            thumbnail = f"https://images.gameinfo.io/pokemon/256/{dex_no.zfill(3)}-00.png"

            best_versions = discord.Embed(color=0xFF0000, timestamp=datetime.utcnow())
            best_versions.set_author(name=f"{pokemon} - #{dex_no}",
                                     icon_url=icon)
            best_versions.add_field(name=f"100 IV variants of {pokemon}", value="\u200b", inline=False)
            best_versions.add_field(name="""Level        CP""", value="\u200b", inline=False)
            for level, multiplier in self.multipliers.items():  # Ugly spacing required for embed format
                best_versions.add_field(
                    name=f"""{level}             {int((stats[0] * stats[1] ** 0.5 * stats[2] ** 0.5 * multiplier ** 2) // 10)}""",
                    value="\u200b",
                    inline=False)
            best_versions.set_thumbnail(url=thumbnail)
            if channel.lower() == "public":
                await ctx.send(embed=best_versions)
            else:
                await ctx.message.author.send(embed=best_versions)
        except KeyError:
            await ctx.message.author.send(f"'{pokemon}' is not a valid Pokemon or is not yet recognised")


def setup(client):
    client.add_cog(Calculator(client))
