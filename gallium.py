import os
from utils.bot import Gallium
import json

tokenFile = "utils/config.json"
with open(tokenFile) as f:
    data = json.load(f)
token = data["TOKEN"]

excluded = [
    "checks.py",
    "formats.py",
    "__init__.py",
    "paginator.py",
    "time.py",
    "del.py",
    "bancheck.py",
]

bot = Gallium()


os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

# also
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

"""
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename not in excluded:
        bot.load_extension(f"cogs.{filename[:-3]}")
        bot.log.info(f"Loaded cog {filename[:-3]}")
"""
bot.load_extension("cogs.dev")
bot.log.info("Loaded cog dev")
bot.load_extension("cogs.meta")
bot.log.info("Loaded cog meta")
bot.load_extension("cogs.settings")
bot.log.info("Loaded cog settings")

bot.load_extension("jishaku")

bot.run(token)
