import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, specific=None):
        """Displays this message"""
        await ctx.message.delete()
        help_message = discord.Embed(color=0x8B008B)
        help_message.set_author(name="Professor Oak - Help", icon_url=self.client.user.avatar_url)
        for cog in self.client.cogs:
            for command in self.client.get_cog(cog).get_commands():
                help_message.add_field(name=str(command).capitalize(), value=command.help)

        await ctx.message.author.send(embed=help_message)


def setup(client):
    client.add_cog(Help(client))
