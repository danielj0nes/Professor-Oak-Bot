from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup, NavigableString


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["events", "e", "Event", "Events"])
    @commands.has_permissions(administrator=True)
    async def event(self, ctx, channel=""):
        """Displays a list of current and upcoming Pokémon GO events.
        **Example**: `!event`."""
        await ctx.message.delete()
        URL = "https://leekduck.com/events/"
        page_source = requests.get(URL)
        soup = BeautifulSoup(page_source.text, "html.parser")
        event_embed = discord.Embed(color=0x8B008B)
        event_embed.set_author(name="Professor Oak - Current & Upcoming Events", icon_url=self.client.user.avatar_url)
        for i in soup.find("div", {"class": "events-list current-events"}):
            if isinstance(i, NavigableString):
                continue
            else:
                event_url = f"{URL[:-8]}{i['href']}"
                event_embed.add_field(name="\u200b", value=f"[{i.find('h2').text}]({event_url})")
        event_embed.set_footer(text="If you want to help support the development of the bot, consider "
                                    "donating over at: paypal.me/danielltd")
        if channel.lower() == "public":
            await ctx.send(embed=event_embed)
        else:
            await ctx.message.author.send(embed=event_embed)


def setup(client):
    client.add_cog(Events(client))
