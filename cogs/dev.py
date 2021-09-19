import discord

from .utils import checks
import aiohttp
import logging
import traceback
import os
import io
from aiohttp_requests import requests
from discord.ext import commands
from discord.app import slash_command

from jishaku.codeblocks import codeblock_converter

import subprocess as sp

from pymongo import MongoClient

from typing import Union

log = logging.getLogger("titanium.cog_loader")


class dev(discord.Cog):
    """Developer Commands"""

    def __init__(self, bot):
        self.bot = bot
        mcl = MongoClient()
        self.trusted = mcl.Gallium.trusted
        self.footer = bot.footer
        self.color = bot.color

    @commands.is_owner()
    @slash_command()
    async def load(self, ctx, name: str):
        """Loads an extension. """
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            etype = type(e)
            trace = e.__traceback__
            lines = traceback.format_exception(etype, e, trace)
            goodtb = "".join(lines)
            r = await requests.post("https://hastebin.com/documents", data=goodtb)
            re = await r.json()
            return await ctx.respond(f"https://hastebin.com/{re['key']}")
        await ctx.respond(f"📥 Loaded extension **cogs/{name}.py**")

    @commands.is_owner()
    @slash_command(aliases=["r"])
    async def reload(self, ctx, name: str):
        """Reloads an extension. """

        try:
            self.bot.reload_extension(f"cogs.{name}")
            await ctx.respond(f"🔁 Reloaded extension **cogs/{name}.py**")

        except Exception as e:
            etype = type(e)
            trace = e.__traceback__
            lines = traceback.format_exception(etype, e, trace)
            goodtb = "".join(lines)
            r = await requests.post("https://hastebin.com/documents", data=goodtb)
            re = await r.json()
            return await ctx.respond(f"https://hastebin.com/{re['key']}")

    @commands.is_owner()
    @slash_command()
    async def unload(self, ctx, name: str):
        """Unloads an extension. """
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.respond(f"```py\n{e}```")
            log.error(e)
        await ctx.respond(f"📤 Unloaded extension **cogs/{name}.py**")

    @commands.is_owner()
    @slash_command(aliases=["ra"])
    async def reloadall(self, ctx):
        """Reloads all extensions. """
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    etype = type(e)
                    trace = e.__traceback__
                    lines = traceback.format_exception(etype, e, trace)
                    goodtb = "".join(lines)
                    r = await requests.post(
                        "https://hastebin.com/documents", data=goodtb
                    )
                    re = await r.json()
                    return await ctx.respond(f"https://hastebin.com/{re['key']}")

        if error_collection:
            output = "\n".join(
                [f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection]
            )
            return await ctx.respond(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        return await ctx.respond("Successfully reloaded all extensions")

    @commands.is_owner()
    @slash_command()
    async def leaveguild(self, ctx):
        """Leave the current server."""
        embed = discord.Embed(title="Goodbye", color=self.color)
        embed.set_footer(text=self.footer)
        await ctx.respond(embed=embed)
        await ctx.guild.leave()
        log.info(f"Left {ctx.guild}, ID: {ctx.guild.id} at owners request.")

    @commands.is_owner()
    @slash_command()
    async def status(self, ctx, type, *, status=None):
        """Change the Bot Status"""
        if type == "playing":
            await self.bot.change_presence(activity=discord.Game(name=f"{status}"))
            await ctx.respond(f"Changed status to `Playing {status}`")
        elif type == "listening":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening, name=f"{status}"
                )
            )
            await ctx.respond(f"Changed status to `Listening to {status}`")
        elif type == "watching":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=f"{status}"
                )
            )
            await ctx.respond(f"Changed status to `Watching {status}`")
        elif type == "bot":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=f"{len(self.bot.users)} users in {len(self.bot.guilds)} servers",
                )
            )
            await ctx.respond(
                f"Changed status to `Watching {len(self.bot.users)} users in {len(self.bot.guilds)} servers`"
            )
        elif type == "competing":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.competing, name=f"{status}"
                )
            )
            await ctx.respond(f"Changed status to `Competing in {status}`")
        elif type == "streaming":
            await self.bot.change_presence(
                activity=discord.Streaming(
                    name=f"{status}", url="https://www.twitch.tv/elevatebot"
                )
            )
            await ctx.respond(f"Changed status to `Streaming {status}`")
        elif type == "reset":
            await self.bot.change_presence(status=discord.Status.online)
            await ctx.respond("Reset Status")
        else:
            await ctx.respond(
                "Type needs to be either `playing|listening|watching|streaming|competing|bot|reset`"
            )

    @commands.is_owner()
    @slash_command()
    async def dm(self, ctx, user: discord.Member, *, content):
        """Dm a Member"""
        embed = discord.Embed(color=self.color)
        embed.set_author(name=f"Sent from {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Message:", value=f"{content}")
        embed.set_footer(text=self.footer)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/726779670514630667.png?v=1"
        )
        await user.send(embed=embed)
        await ctx.respond(f"<:comment:726779670514630667> Message sent to {user}")

    @commands.is_owner()
    @slash_command(aliases=["ss"])
    async def screenshot(self, ctx, url):
        await ctx.respond("This is a slow API so it may take some time.")
        embed = discord.Embed(title=f"Screenshot of {url}", color=self.color)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://image.thum.io/get/width/1920/crop/675/maxAge/1/noanimate/{url}"
            ) as r:
                res = await r.read()
            embed.set_image(url="attachment://ss.png")
            embed.set_footer(text=self.footer)

            await ctx.respond(
                file=discord.File(io.BytesIO(res), filename="ss.png"), embed=embed
            )

    @commands.is_owner()
    @slash_command()
    async def say(self, ctx, *, content: str):
        """Make the bot say something"""
        await ctx.respond(content)

    @commands.is_owner()
    @slash_command(aliases=["e"])
    async def eval(self, ctx, *, code: str):
        """Evaluate code"""
        cog = self.bot.get_cog("Jishaku")
        res = codeblock_converter(code)
        await cog.jsk_python(ctx, argument=res)

    @slash_command()
    @commands.is_owner()
    async def nick(self, ctx, *, name: str):
        try:
            await ctx.guild.me.edit(nick=name)
            await ctx.respond(f"Successfully changed username to **{name}**")
        except discord.HTTPException as err:
            await ctx.respond(f"```{err}```")

    @slash_command()
    @commands.is_owner()
    async def rn(self, ctx):
        await ctx.guild.me.edit(nick=None)
        await ctx.respond("Nickname reset to Gallium")

    @commands.is_owner()
    @slash_command(aliases=["la"])
    async def loadall(self, ctx):
        """Reloads all extensions. """
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.load_extension(f"cogs.{name}")
                except Exception as e:
                    return await ctx.respond(f"```py\n{e}```")
                    log.error(e)

        if error_collection:
            output = "\n".join(
                [f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection]
            )
            return await ctx.respond(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        await ctx.respond("Successfully reloaded all extensions")

    @slash_command(aliases=["s"])
    @commands.is_owner()
    async def sync(self, ctx):
        """Sync with GitHub and reload all the cogs"""
        embed = discord.Embed(
            title="Syncing...",
            description="Syncing and reloading cogs.",
            color=self.color,
        )
        embed.set_footer(text=self.footer)
        msg = await ctx.respond(embed=embed)
        async with ctx.channel.typing():
            sp.getoutput("git pull")
            embed = discord.Embed(
                title="Synced",
                description="Synced with GitHub and reloaded all the cogs.",
                color=self.color,
            )
            # Reload Cogs as well
            error_collection = []
            for file in os.listdir("cogs"):
                if file.endswith(".py"):
                    name = file[:-3]
                    try:
                        self.bot.reload_extension(f"cogs.{name}")
                    except Exception as e:
                        return await ctx.respond(f"```py\n{e}```")

            if error_collection:
                err = "\n".join(
                    [f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection]
                )
                return await ctx.respond(
                    f"Attempted to reload all extensions, was able to reload, "
                    f"however the following failed...\n\n{err}"
                )

            await msg.edit(embed=embed)

    # TODO: fix once the db works
    """    
    @slash_command()
        @commands.is_owner()
        async def addtrusted(
            self, ctx, user: Union[discord.User, discord.Member], reason=None
        ):
            Add a user to the trusted list
            doc = self.trusted.find_one({"_id": user.id})
            if doc and doc.get("trusted"):
                await ctx.respond("That user is already trusted!")
            elif doc:
                self.trusted.update_one(
                    query={"_id": user.id},
                    update={"$set": {"trusted": True, "reason": reason}},
                )
                await ctx.respond("I've successfully updated that user's trusted status")
            elif not doc:
                self.trusted.insert_one({"_id": user.id, "trusted": True, "reason": reason})
                await ctx.respond("That user is now trusted!")
    

    @slash_command()
    @checks.is_trusted()
    async def trusted(self, ctx):
        await ctx.respond("You are trusted")
    """


def setup(bot):
    bot.add_cog(dev(bot))
