"""Daniel Jones"""
# https://discordapp.com/oauth2/authorize?client_id=753011266187952288&scope=bot&permissions=8
import discord
from database.db import SQL
from discord.ext import commands
from pathlib import Path

sql = SQL()
print(f"Using discord.py version {discord.__version__}")
client = commands.Bot(command_prefix=sql.get_prefix)
client.remove_command("help")

with open("token.txt", "r") as f:
    tkn = f.readline()


@client.event
async def on_guild_join(guild):
    sql.add_prefix(guild.id, "!")  # Default prefix set upon bot joining the server


@client.event
async def on_command_error(ctx, error):
    """Handle console spam from frequent error types"""
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.author.send(error)
        return
    raise error


@client.command()
async def load(ctx, extension):
    """The load/reload functions are purely for debugging.
    These allow for loading new / reloading existing extensions on the fly."""
    if ctx.message.author.id == 93863518389932032:
        await ctx.message.delete()
        client.load_extension(f"cogs.{extension}")


@client.event
async def on_message(message):
    if "<@!753011266187952288>" in message.content:  # Handle bot mentions
        server_prefix = sql.get_prefix(message, message)[0]
        await message.author.send(f"Hello trainer! To access my commands, start your message with"
                                  f"`{server_prefix}`. For more information, try `{server_prefix}help`.")
    await client.process_commands(message)


@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id == 93863518389932032:
        await ctx.message.delete()
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")


for cog in Path("cogs/").iterdir():
    if cog.suffix == ".py":
        client.load_extension(f"cogs.{cog.stem}")


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Game("PoKéMoN GO"))


client.run(tkn)
