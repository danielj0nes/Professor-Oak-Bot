from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup, NavigableString


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["events", "e", "Event", "Events"])
    @commands.has_permissions(administrator=True)
    async def event(self, ctx, channel="", all=""):
        """Displays a list of current and upcoming Pokémon GO events.
        **Example**: `!event`."""
        counter = 0
        URL = "https://leekduck.com/events/"
        page_source = requests.get(URL)
        soup = BeautifulSoup(page_source.text, "html.parser")
        event_embed = discord.Embed(color=0x8B008B)
        event_embed.set_author(name="Professor Oak - Current & Upcoming Events", icon_url=self.client.user.avatar_url)
        if not all:
            event_embed.add_field(name="\u200b", value="**Note**: for a full list of events, "
                                                       "add 'all' to the end of the command", inline=False)
        for i in soup.find("div", {"class": "events-list current-events"}):
            if isinstance(i, NavigableString):
                continue
            else:
                counter += 1
                if not all:
                    if counter <= 9:
                        event_url = f"{URL[:-8]}{i['href']}"
                        event_embed.add_field(name="\u200b", value=f"[{i.find('h2').text}]({event_url})")
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
