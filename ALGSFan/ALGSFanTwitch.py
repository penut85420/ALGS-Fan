# python -m ALGSFan.ALGSFanTwitch

import asyncio
import sys

from loguru import logger
from twitchio.ext import commands
from twitchio.ext.commands.errors import CommandNotFound

from ALGSFan import ALGSSheet, LiquipediaSearchNextMatch, TWSCCalendar
from ALGSFan.Utils import load_json, set_logger


class ALGSFan(commands.Bot):
    def __init__(self, logfile=sys.stdout, verbose=True):
        self.config = load_json("Config.json")["twitch_bot"]
        self.threshold = self.config["threshold"]
        self.logfile = logfile
        self.verbose = verbose
        self.channel_list = self.config["channels"]
        self.channel_count = {channel: 0 for channel in self.channel_list}
        super().__init__(
            token=self.config["token"],
            prefix=self.config["prefix"],
            initial_channels=list(self.channel_list),
        )
        self.tc = TWSCCalendar()

        for sheet_info in self.config["sheet_info"]:
            name = f"sheet_{sheet_info[2].lower()}"
            setattr(self, name, ALGSSheet(*sheet_info))

        for k in self.config["simple_command"]:
            cmd = commands.command(name=k)(self.mk_command(k))
            self.add_command(cmd)

    async def reload_commands(self):
        while True:
            try:
                for k in self.config["simple_command"]:
                    self.rm_command(k)
                self.config = load_json("Config.json")["twitch_bot"]
                for k in self.config["simple_command"]:
                    cmd = commands.command(name=k)(self.mk_command(k))
                    self.add_command(cmd)
            except Exception as e:
                logger.error(str(e))

            await asyncio.sleep(self.config["timer"]["command_reload"])

    def rm_command(self, k):
        try:
            self.remove_command(k)
        except:
            pass

    def mk_command(self, k):
        async def f(ctx):
            await ctx.send(self.config["simple_command"][k])

        return f

    def log(self, msg):
        self.logfile.info(msg.replace("\n", " "))

    async def event_ready(self):
        self.log(f"Ready | {self.nick}")

        tasks = [
            self.mk_timer_event(
                self.config["main_channel"],
                self.pos_msg,
                self.config["timer"]["main_channel_timer"],
            ),
            self.mk_timer_event(
                None,
                self.tc.get_next_event,
                self.config["timer"]["next_event_timer"],
            ),
            self.reload_commands,
        ]
        tasks = [asyncio.get_event_loop().create_task(t()) for t in tasks]

    def mk_timer_event(self, target_channels, msg_fn, sleep_time):
        async def timer_event():
            while True:
                async for ch in self.iter_channel(target_channels):
                    await ch.send(msg_fn())
                await asyncio.sleep(sleep_time)

        return timer_event

    async def iter_channel(self, target=None):
        if target is None:
            target = self.channel_count

        for ch_name, count in self.channel_count.items():
            if ch_name in target and count > self.threshold:
                self.channel_count[ch_name] = 0
                channel = self.get_channel(ch_name)
                if channel is None:
                    await self.join_channels(ch_name)
                    channel = self.get_channel(ch_name)
                yield channel

    async def event_message(self, msg):
        if msg.author is None:
            return

        self.log(f"[{msg.channel.name}] {msg.author.name}: {msg.content}")
        msg.content = msg.content.lower()
        msg.content = msg.content.replace("！", "!")

        if str(msg.channel) in self.channel_count:
            self.channel_count[str(msg.channel)] += 1

        await self.handle_commands(msg)

    async def event_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            msg = f"Command {ctx.message.content} Not Found"
            self.log(msg)
        else:
            self.log(str(error).replace("\n", " | "))

    @commands.command(name="藍兔2021")
    async def algs_2021(self, ctx):
        await ctx.send(self.anniversary_msg())

    @commands.command(name="支持")
    async def zeczec_pos(self, ctx):
        await ctx.send(self.pos_msg())

    def anniversary_msg(self):
        return (
            "【2021 藍兔葉克膜年度大回饋總名單】  "
            "https://algssc2.pse.is/3vg9nf  "
            "付費大大們快來核對你的愛心抽獎點數是不是符合唷！"
            "如果有缺漏請在1/15直播開抽前把付款收據出示給我們 <3"
        )

    def pos_msg(self):
        return (
            "星途或許顛簸，但有你的加入，一切將變得更順遂。"
            "最直接地支持我們製作更多精彩的《星海爭霸II》內容 - "
            "https://www.zeczec.com/projects/pathofstar"
        )

    @commands.command(name="星海比賽", aliases=["比賽", "b", "bracket", "賽程", "賽程表"])
    async def calendar(self, ctx):
        await ctx.send(self.tc.get_next_event())

    @commands.command(name="下一場比賽", aliases=["nt"])
    async def next(self, ctx):
        await ctx.send(self.tc.get_next_event(next_only=True))

    @commands.command(name="報名")
    async def sign(self, ctx):
        await ctx.send(self.tc.get_next_sign())

    @commands.command(name="哈囉")
    async def testing(self, ctx):
        await ctx.send(f"{ctx.author.name} 你好啊!")

    @commands.command(
        name="藍兔", aliases=["algs", "dc", "dis", "link", "連結", "歐付寶", "donate"]
    )
    async def algs(self, ctx):
        await ctx.send(self.sheet_algs.get_msg())

    @commands.command(name="召喚")
    async def cmd_summon(self, ctx, *arg):
        player = " ".join(arg).strip()
        if player == "":
            await ctx.send("指令格式：`!召喚 [選手名稱]`")
            return

        result = LiquipediaSearchNextMatch(player)
        await ctx.send(result)

    @commands.command(name="nice")
    async def cmd_nice(self, ctx):
        await ctx.send(self.sheet_nice.get_msg())

    @commands.command(name="rex")
    async def cmd_rex(self, ctx):
        await ctx.send(self.sheet_rex.get_msg())

    @commands.command(name="nice比賽")
    async def cmd_nice_match(self, ctx):
        msg = LiquipediaSearchNextMatch("Nice")
        await ctx.send(msg)

    @commands.command(name="rex比賽")
    async def cmd_rex_match(self, ctx):
        msg = LiquipediaSearchNextMatch("Rex")
        await ctx.send(msg)

    @commands.command(name="has比賽")
    async def cmd_has_match(self, ctx):
        msg = LiquipediaSearchNextMatch("Has")
        await ctx.send(msg)


if __name__ == "__main__":
    set_logger()
    ALGSFan(logfile=logger).run()
