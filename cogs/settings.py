from discord.ext import commands
import discord
from pymongo import MongoClient
from typing import Union

off = "<:xon:792824364658720808><:coff:792824364483477514>"
on = "<:xoff:792824364545605683><:con:792824364558843956>"


class config(commands.Cog):
    """Settings for Elevate"""

    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        db = mcl.Gallium
        self.prfx = db.prefixes
        self.welcome = db.welcome

    @commands.group(aliases=["set"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        """Change Gallium's settings"""
        if not ctx.invoked_subcommand:
            emb = discord.Embed(title="Settings for Gallium", color=ctx.bot.color)
            await ctx.respond_help(ctx.command)

    @settings.command()
    async def prefix(self, ctx, *, prefix: str = None):
        """Set Elevate's prefix. If no prefix is specified, the prefix will be reset to default."""
        doc = self.prfx.find_one({"_id": ctx.guild.id})
        if not doc:
            if prefix and not doc:
                self.prfx.insert_one({"_id": ctx.guild.id, "prfx": prefix})
                await ctx.respond(f"Successfully set the server prefix to {prefix}")
                return
            elif not prefix:
                await ctx.respond("You didn't specify a prefix!")
                return
        elif doc:
            if not prefix and not doc.get("prfx"):
                await ctx.respond("You didn't specify a prefix!")
                return
            elif not prefix and doc.get("prfx"):
                self.prfx.update_one(
                    filter={"_id": ctx.guild.id}, update={"$unset": {"prfx": ""}}
                )
                await ctx.respond("Prefix cleared")
                return
            else:
                self.prfx.update_one(
                    filter={"_id": ctx.guild.id}, update={"$set": {"prfx": prefix}}
                )
                await ctx.respond(f"Successfully set the server prefix to {prefix}")
                return


def setup(bot):
    bot.add_cog(config(bot))
