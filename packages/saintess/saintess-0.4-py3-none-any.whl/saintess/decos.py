from discord.ext import commands
from discord import app_commands

def saintess(name, desc):
    def decorator(func):
        return commands.hybrid_command(name=name, description=desc)(func)
    return decorator

def guild(enabled, user):
    def decorator(func):
        return app_commands.allowed_installs(guilds=enabled, users=user)(func)
    return decorator

def user(guild, dms, private):
    def decorator(func):
        return app_commands.allowed_contexts(guilds=guild, dms=dms, private_channels=private)(func)
    return decorator
