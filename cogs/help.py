import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        """Displays this message.
        **Example**: `!help`"""
        help_message = discord.Embed(color=0x8B008B)
        help_message.set_author(name="Professor Oak - Help", icon_url=self.client.user.avatar_url)
        help_message.add_field(name="\u200b", value="Got a question? Want a specific feature added to the bot? "
                                                    "Get in touch through discord directly: **daniel󠀀󠀀 󠀀󠀀#2819**")
        for cog in self.client.cogs:
            for command in self.client.get_cog(cog).get_commands():
                help_message.add_field(name=str(command).capitalize(), value=command.help, inline=False)
        help_message.set_footer(text="If you want to help support the development of the bot, consider "
                                     "donating over at: paypal.me/danielltd")
        await ctx.message.author.send(embed=help_message)


def setup(client):
    client.add_cog(Help(client))
