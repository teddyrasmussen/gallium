import discord
from discord.ext import commands
import platform
import sys
import psutil
import aiohttp
import os
import distro


class Gallium(commands.Cog):
    """Information about Gallium"""

    def __init__(self, bot):
        self.bot = bot
        self.color = bot.color
        self.footer = bot.footer

    @commands.command()
    async def vote(self, ctx):
        """Vote for Gallium on top.gg"""
        embed = discord.Embed(
            title="Vote",
            description="**Vote for Gallium [here](https://top.gg/bot/716798638277525535/vote)",
            color=self.color,
        )
        embed.set_footer(text=self.footer)
        await ctx.respond(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Get the invite for the bot."""
        emb = discord.Embed(
            title="Invite Gallium",
            description="Invite me [here](https://discord.com/oauth2/authorize?client_id=888557582262886450&scope=bot&permissions=402713846t) with permissions, or [here](https://discord.com/oauth2/authorize?client_id=888557582262886450&scope=bot&permissions=0) without permissions",
            color=self.color,
        )
        emb.set_footer(text=self.footer)
        await ctx.respond(embed=emb)

    @commands.command(aliases=["info"])
    async def about(self, ctx):
        """Get info about Gallium"""
        emb = discord.Embed(
            title="Gallium Info",
            description="A simple Discord bot with moderation tools and music",
            color=self.color,
            url="https://github.com/CraziiAce/Gallium",
        )
        emb.set_author(
            name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
        )
        emb.add_field(
            name="News",
            value=f"**:wave: Gallium has alt detection!",
            inline=True,
        )
        emb.add_field(
            name=":link: Links",
            value="[Invite Gallium](https://discord.com/oauth2/authorize?client_id=888557582262886450&scope=bot&permissions=402713846t)",
            inline=False,
        )
        emb.set_footer(text=self.footer)
        await ctx.respond(embed=emb)

    @commands.command()
    async def support(self, ctx):
        """Get support information."""
        supportembed = discord.Embed(title="Gallium support", color=self.color)
        supportembed.set_author(
            name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
        )
        supportembed.add_field(
            name="Support Server",
            value="<a:igloading:737723292768796713> Support Server: https://discord.gg/zwyFZ7h",
            inline=False,
        )
        supportembed.add_field(
            name="Contact",
            value="To contact support staff, use `g!support <message>`",
            inline=False,
        )
        supportembed.set_footer(text=f"Use {ctx.prefix}help or info for more")
        await ctx.respond(embed=supportembed)

    @commands.command()
    async def stats(self, ctx):
        """Get stats for Gallium"""
        dpy = discord.version_info
        d = distro.linux_distribution()
        ld = d[0] + " " + d[1]
        is_linux = sys.platform == "linux"
        is_windows = os.name == "nt"
        embed = discord.Embed(
            title="Gallium Stats",
            color=self.color,
            description="Gallium | The only Discord bot you'll ever need\nDeveloped by CraziiAce#0001",
        )
        embed.add_field(
            name="Python stats",
            value=f"Python version: **{platform.python_version()}**\ndiscord.py version: **{dpy.major}.{dpy.minor}.{dpy.micro}-{dpy.releaselevel}**\naiohttp version: **{aiohttp.__version__}**",
        )
        embed.add_field(
            name="Bot stats",
            value=f"Servers: **{len(ctx.bot.guilds)}\n**Users: **{len(ctx.bot.users)}**\nEmojis: **{len(ctx.bot.emojis)}**\nCommands: **{len(ctx.bot.commands)}**",
            inline=False,
        )
        embed.set_footer(text=self.footer)
        if is_linux:
            embed.add_field(
                name="Server stats",
                value=f"CPU current clockspeed: **{round(psutil.cpu_freq().current / 1000, 2)} GHz**\nCPU max clockspeed: **{round(psutil.cpu_freq().max / 1000, 2)} GHz**\nCPU usage: **{psutil.cpu_percent()}%\n**RAM:** {round(psutil.virtual_memory().total / 1000000)} MB\n**RAM usage:** {psutil.virtual_memory().percent}%**\nOperating system: **{platform.system()}**\nOS version: **{ld}**",
                inline=False,
            )
        elif is_windows:
            embed.add_field(
                name="Server stats",
                value=f"CPU current clockspeed: **{round(psutil.cpu_freq().current / 1000, 2)} GHz**\nCPU max clockspeed: **{round(psutil.cpu_freq().max / 1000, 2)} GHz**\nCPU usage: **{psutil.cpu_percent()}%\n**RAM:** {round(psutil.virtual_memory().total / 1000000)} MB\n**RAM usage:** {psutil.virtual_memory().percent}%**\nOperating system: **{platform.system()}**\nOS version: **{platform.platform()}**",
                inline=False,
            )
        await ctx.respond(embed=embed)

    @commands.command()
    async def privacy(self, ctx):
        """Get my privacy policy"""
        await ctx.respond(
            "Gallium takes your privacy very seriously. We only store data that is necessary to the operation of Gallium, like user IDs, guild IDs, role IDs, and channel IDs. Gallium accesses more extensive data on users, roles, guilds, and channels when certain commands are run, but it is not stored.\nThe data Gallium collects is stored only on the secure, password- and private-key protected servers that Gallium is run on, and except for some command arguments, is never sent anywhere.\n If you have any questions, DM CraziiAce#0001 on Discord"
        )

    @commands.command()
    async def credits(self, ctx):
        """Get Gallium's credits"""
        emb = discord.Embed(
            title="Credits",
            description="**Lead developer:** CraziiAce#0001\n**Help command & cog loader:** isirk#0001",
            color=self.color,
        )
        emb.set_footer(text=self.footer)
        await ctx.respond(embed=emb)

    @commands.command()
    async def donate(self, ctx):
        """Donate to Gallium!"""
        emb = discord.Embed(
            title="Donate to Gallium! All donations are greatly appreciated.",
            url=f"https://donatebot.io/checkout/718663089318527016?buyer={ctx.author.id}",
        )
        await ctx.respond(embed=emb)


def setup(bot):
    bot.add_cog(Gallium(bot))
