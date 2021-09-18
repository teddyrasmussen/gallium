import discord
from discord.ext import commands
from datetime import datetime
import aiohttp
from pymongo import MongoClient
import json
import logging


prefixFile = "utils/tools.json"
with open(prefixFile) as f:
    data = json.load(f)
prefixes = data["PREFIXES"]
color = int(data["COLORS"], 16)
footer = str(data["FOOTER"])


intents = discord.Intents.default()
intents.members = True

mcl = MongoClient()

log = logging.getLogger("gallium.core")
logging.basicConfig(
    level=logging.INFO,
    datefmt="%I:%M %p on %B %d %Y",
    format="%(asctime)s:%(levelname)s: %(name)s: %(message)s",
)


class Gallium(commands.Bot):
    """
    Main bot subclass
    """

    def __init__(self):
        super().__init__(
            command_prefix=self.get_pre,
            intents=intents,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(
                users=True, roles=True, everyone=False, replied_user=False
            ),
            owner_id=555709231697756160,
            description="The only discord bot you'll ever need.",
        )
        self.start_time = datetime.utcnow()
        self.session = aiohttp.ClientSession()
        self.footer = footer
        self.color = color
        self.db = mcl.Gallium
        self.supportathrids = []
        self.supportchnlids = []
        self.log = log

    def __str__():
        return "Gallium | Moderation, Alt Detection & more."

    def get_pre(self, bot, message):        
        prfx = self.db.prefixes
        if message.guild:
            doc = prfx.find_one({"_id": message.guild.id})
            if doc and doc.get("prfx"):
                return doc.get("prfx")
            else:
                return prefixes
        else:
            return prefixes

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.author.id == self.owner_id:
            await self.process_commands(after)

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.process_commands(message)
        if "<@!763851389403136020>" in message.content:
            if self.get_pre(self, message) == prefixes:
                embed = discord.Embed(
                    title="Gallium",
                    description="Hey there :wave:! Seems like you mentioned me.\n\nMy prefixes are `g!` and `allium`. \nIf you would like to see my commands, type `t!help`",
                    color=0x2F3136,
                )
            else:
                embed = discord.Embed(
                    title="Gallium",
                    description=f"Hey there :wave:! Seems like you mentioned me.\n\nMy prefix is `{str(await self.get_pre(bot=self, messsage=message))}` \nIf you would like to see my commands, type `{str(await self.get_pre(self, message))}help`",
                    color=0x2F3136,
                )

            await message.channel.send(embed=embed)

    @commands.command()
    async def supportrequest(self, ctx, *, msg: str):
        """Send a message to my support team!"""
        emb = discord.Embed(
            title="Support Request!",
            description=f"Message: {msg}\nAuthor ID to reply: {ctx.author.id}",
        )
        time = datetime.datetime.now()
        time = time.strftime("%b %d at %I:%M %p")
        emb.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        emb.set_footer(text=f"New support request by {ctx.author} on {time}")
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(
                "https://canary.discord.com/api/webhooks/764934046940659762/sJOO0N6O2MHqRxpr1LyWRfPgBFzcyBFe1CnXV4gJ4OqmWWcx-Z49DZBAPceiixOZjDkA",
                adapter=discord.AsyncWebhookAdapter(session),
            )
            await webhook.send(
                embed=emb,
                username=ctx.author.name,
                avatar_url=ctx.author.avatar_url,
            )
        await ctx.send("Message sent!")
        self.supportathrids.append(ctx.author.id)
        self.supportchnlids.append(ctx.channel.id)

    @commands.command()
    @commands.has_role(764306292675969029)
    async def replysupport(self, ctx, userid: int, *, msg: str):
        for id in self.supportathrids:
            if id == userid:
                channel = self.get_channel(
                    self.supportchnlids[self.supportathrids.index(id)]
                )
                emb = discord.Embed(
                    title="Support Message!",
                    description=f"My support team has asked me to send you this message:\n{msg}",
                )
                emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await channel.send(f"<@!{userid}>")
                await channel.send(embed=emb)
                self.supportathrids.remove(id)
                self.supportchnlids.pop(self.supportathrids.index(id))
        await ctx.send("📤 Message sent!")

    @commands.command(aliases=["shutdown"])
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.send("👋 Bye!")
        await self.close()
        log.info("Gallium exited with exit code 0 (intentional)")
