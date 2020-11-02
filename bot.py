# https://discordapp.com/oauth2/authorize?client_id=753011266187952288&scope=bot&permissions=8
import discord
from database.db import SQL
from discord.ext import commands
from pathlib import Path

sql = SQL()
TKN = ""  # Don't forget to remove this ;-)
print(f"Using discord.py version {discord.__version__}")
client = commands.Bot(command_prefix=sql.get_prefix)
client.remove_command("help")  # The bot has it's own custom help command, so the default help command is removed


@client.event
async def on_guild_join(guild):
    sql.add_prefix(guild.id, "!")  # Default prefix set upon bot joining the server
    await guild.text_channels[0].send(f"Hello trainers! To use a command, start your message with "
                                      f"`!`. For a full list of commands, try `!help`.")


@client.event
async def on_message(message):
    if "<@!753011266187952288>" in message.content:  # Handle bot mentions
        server_prefix = sql.get_prefix(message, message)[0]
        await message.channel.send(f"Hello trainer! To use a command, start your message with "
                                   f"`{server_prefix}`. For a full list of commands, try `{server_prefix}help`.")
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    """Handle console spam from frequent error types"""
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.author.send(error)
        return
    if isinstance(error, commands.CommandInvokeError):
        await ctx.message.author.send("The bot is missing required permissions.")
        return
    raise error


@client.command()
async def load(ctx, extension):
    """The load/reload functions are purely for debugging.
    These allow for loading new / reloading existing extensions on the fly."""
    if ctx.message.author.id == 93863518389932032:
        client.load_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id == 93863518389932032:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")


for cog in Path("cogs/").iterdir():
    if cog.suffix == ".py":
        client.load_extension(f"cogs.{cog.stem}")


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Game("PoKéMoN GO"))


client.run(TKN)
