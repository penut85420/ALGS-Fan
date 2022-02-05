# python -m ALGSFan.ALGSFanDiscord

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from loguru import logger

from ALGSFan import ALGSSheet, LiquipediaSearchNextMatch, TWSCCalendar
from ALGSFan.Utils import load_json, set_logger

config = load_json("Config.json")

bot = commands.Bot(
    command_prefix=config["twitch_bot"]["prefix"],
    help_command=None,
    case_insensitive=True,
    activity=discord.Activity(
        name=config["discord_bot"]["activity"],
        type=discord.ActivityType.playing,
    ),
)

tc = TWSCCalendar()


def add_simple_cmd(name, msg):
    @bot.command(name=name)
    async def _(ctx):
        await ctx.send(msg)


for k, v in config["twitch_bot"]["simple_command"].items():
    add_simple_cmd(k, v)


@bot.event
async def on_ready():
    logger.info(f"Ready | {bot.user}")


@bot.event
async def on_message(ctx):
    msg = ctx.content.replace("\n", " ")

    if ctx.content.startswith("!"):
        logger.info(f"{ctx.author}: {msg}")

    if ctx.author == bot.user:
        logger.info(f"{ctx.author}: {msg}")

    if bot.user in ctx.mentions:
        await ctx.channel.send(
            "`!近期比賽` 可以列出最近的星海比賽\n"
            "`!近期可報名` 可以列出最近可以報名的星海比賽\n\n"
            "其他指令請參考 https://git.io/JJuba\n"
            "邀請藍兔小粉絲加入你的 Discord 群組 <https://tinyurl.com/ALGS-Fan>"
        )

    await commands.Bot.on_message(bot, ctx)


@bot.event
async def on_command_error(_, error):
    if isinstance(error, CommandNotFound):
        return
    logger.error(str(error).replace("\n", " | "))


@bot.command(name="近期比賽")
async def cmd_recent(ctx):
    await ctx.channel.send(
        "【近期賽事資訊】\n\n"
        f"{tc.get_recent_events()}\n\n"
        "TWSC 星海賽事行事曆\n"
        "<http://bit.ly/TWSCSC2CAL>\n"
        "ALGS 藍兔電子競技工作室 Twitch\n"
        "https://www.twitch.tv/algs_sc2\n"
        "AfreecaTV 艾菲卡 GSL 中文台\n"
        "<http://play.afreecatv.com/gsltw>\n"
        "AfreecaTV 艾菲卡臺灣星海中文轉播台\n"
        "<http://play.afreecatv.com/aftwsc2>\n"
    )


@bot.command(name="近期可報名")
async def cmd_recent_sign(ctx):
    await ctx.channel.send(
        "【近期可報名賽事】\n\n"
        f"{tc.get_recent_sign()}\n\n"
        "若需要協助請洽 https://discord.gg/SwX9KMj"
    )


@bot.command(name="星海比賽", aliases=["比賽", "b", "bracket", "賽程", "賽程表"])
async def cmd_calendar(ctx):
    await ctx.channel.send(tc.get_next_event())


@bot.command(name="下一場比賽", aliases=["nt"])
async def cmd_next(ctx):
    await ctx.channel.send(tc.get_next_event(next_only=True))


@bot.command(name="召喚")
async def cmd_summon(ctx, *arg):
    player = " ".join(arg).strip()
    if player == "":
        await ctx.channel.send("指令格式：`!召喚 [選手名稱]`")
        return

    result = LiquipediaSearchNextMatch(player)
    await ctx.channel.send(result)


@bot.command(name="nice")
async def cmd_nice(ctx):
    nice_name = [
        "死亡鳳凰艦隊提督",
        "抓放軍團最高統帥",
        "冰雪風暴靜滯領主",
        "亞細亞洲璀銀神帝",
        "極限大師廿八星宿",
        "四大毒奶堅持天尊",
    ]
    msg = (
        " <:nice:736140894927061023> ".join(nice_name)
        + " <:nice:736140894927061023>"
    )

    next_match = LiquipediaSearchNextMatch("nice")
    if next_match is not None:
        msg = f"{msg}\n{next_match}"

    await ctx.channel.send(msg)


@bot.command(name="nice比賽")
async def cmd_nice_match(ctx):
    msg = LiquipediaSearchNextMatch("Nice")
    await ctx.channel.send(msg)


@bot.command(name="has比賽")
async def cmd_has_match(ctx):
    msg = LiquipediaSearchNextMatch("Has")
    await ctx.channel.send(msg)


@bot.command(name="rex比賽")
async def cmd_rex_match(ctx):
    msg = LiquipediaSearchNextMatch("Rex")
    await ctx.channel.send(msg)


if __name__ == "__main__":
    set_logger("Logs/algs-discord.log")
    bot.run(config["discord_bot"]["token"])
