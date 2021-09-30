from discord.ext import commands
from discord.app import slash_command
from typing import Union

class Help(commands.Cog):
    """Help Command"""
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def help(self, ctx, thing_to_get_help_for: Union[commands.Cog, commands.slash.Command] = None):
        """Get help for a command or a category"""
        if isinstance(thing_to_get_help_for, commands.Cog):
            await ctx.send(thing_to_get_help_for.help())
        elif isinstance(thing_to_get_help_for, commands.slash.Command):
            await ctx.send(thing_to_get_help_for.help())
        else:
            await ctx.send("That's not a command or a category.")


def setup(bot):
    bot.add_cog(Help(bot))