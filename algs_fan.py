import os
import sys
import asyncio
import threading
import datetime as dt

os.environ['LOGURU_AUTOINIT'] = 'False'
from loguru import logger
from twitchio.ext import commands
from twitchio.ext.commands.errors import CommandNotFound
from twsc_calendar import TWSCCalendar

class ALGSFan(commands.Bot):
    def __init__(self, logfile=sys.stdout, verbose=True):
        self.threshold = 10
        self.logfile = logfile
        self.verbose = verbose
        self.channel_list = os.environ['CHANNEL'].strip().split(',')
        self.channel_count = {channel: self.threshold for channel in self.channel_list}
        super().__init__(
            irc_token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_NICK'],
            prefix='!',
            initial_channels=list(self.channel_list)
        )
        self.tc = TWSCCalendar()

    def log(self, msg):
        self.logfile.info(msg.replace('\n', ' '))

    async def event_ready(self):
        self.log(f'{self.nick} is ready')

        async def timer_next_event():
            while True:
                for ch, count in self.channel_count.items():
                    if count >= self.threshold:
                        self.channel_count[ch] = 0
                        ch = self.get_channel(ch)
                        msg = self.tc.get_next_event()
                        await ch.send(msg)
                await asyncio.sleep(1800)

        async def timer_next_sign():
            while True:
                for ch, count in self.channel_count.items():
                    if count >= self.threshold:
                        self.channel_count[ch] = 0
                        ch = self.get_channel(ch)
                        msg = self.tc.get_next_sign()
                        await ch.send(msg)
                await asyncio.sleep(2400)

        tasks = [timer_next_event, timer_next_sign]
        for i, t in enumerate(tasks):
            tasks[i] = asyncio.create_task(t())

        for t in tasks:
            await t

    async def event_message(self, msg):
        self.log(f'[{msg.author.channel}] {msg.author.name}: {msg.content}')
        msg.content = msg.content.lower()
        if str(msg.author.channel) in self.channel_count and msg.author.name != self.nick:
            self.channel_count[str(msg.author.channel)] += 1
        await self.handle_commands(msg)

    async def event_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            msg = f'Command "{ctx.content}" send from [{ctx.author.channel}] {ctx.author.name} was not found.'
            self.log(msg)
        else:
            self.log(str(error).replace('\n', ' | '))

    @commands.command(name='星海比賽', aliases=['日程', '比賽', 'b', 'bracket', '賽程', '賽程表'])
    async def calendar(self, ctx):
        await ctx.send(self.tc.get_next_event())

    @commands.command(name='下一場比賽', aliases=['nt'])
    async def next(self, ctx):
        await ctx.send(self.tc.get_next_event(next_only=True))

    @commands.command(name='報名')
    async def sign(self, ctx):
        await ctx.send(self.tc.get_next_sign())

    @commands.command(name='hello', aliases=['哈囉'])
    async def testing(self, ctx):
        await ctx.send(f'{ctx.author.name} 你好啊!')

    @commands.command(name='藍兔', aliases=['algs'])
    async def algs(self, ctx):
        await ctx.send('藍兔電子競技工作室臉書粉絲團 https://www.facebook.com/ALGSSC2/')

    @commands.command(name='nice')
    async def nice(self, ctx):
        nice_name = [
            '死亡鳳凰艦隊提督',
            '抓放軍團最高統帥',
            '冰雪風暴靜滯領主',
            '亞細亞洲璀銀神帝',
            '極限大師廿八星宿',
            '四大毒奶堅持天尊'
        ]
        await ctx.send(' GivePLZ '.join(nice_name) + ' GivePLZ ')

    @commands.command(name='az', aliases=['azure'])
    async def az(self, ctx):
        await ctx.send('AZ 大大的臉書粉絲團 https://www.facebook.com/AzureForSC2/')

    @commands.command(name='rex')
    async def rex(self, ctx):
        await ctx.send('Rex 小雷雷臉書粉絲團 https://www.facebook.com/RexStorMWTF')

    @commands.command(name='阿吉')
    async def ahchi(self, ctx):
        await ctx.send('恭迎吉孤觀音⎝༼ ◕д ◕ ༽⎠ 渡世靈顯四方⎝༼ ◕д ◕ ༽⎠')

    @commands.command(name='top')
    async def top(self, ctx):
        await ctx.send('吃我的大火球～～～')

    @commands.command(name='堅持')
    async def persist(self, ctx):
        await ctx.send('你在堅持啥啊')

    @commands.command(name='提告', aliases=['sue'])
    async def sue(self, ctx):
        await ctx.send('Nice：「不排除提告」（設計對白）')

    @commands.command(name='錯覺', aliases=['illusion'])
    async def illusion(self, ctx):
        await ctx.send('你從什麼時候開始產生了你這盤能贏的錯覺？')

    @commands.command(name='釣魚')
    async def fishing(self, ctx):
        await ctx.send('GivePLZ ／︴只有天選之人能釣到這條魚 _________________ SabaPing')

    @commands.command(name='許願')
    async def wish(self, ctx):
        await ctx.send('歡迎到 GitHub 跟小粉絲許願新指令喔！ https://github.com/penut85420/ALGS-Fan')

def set_logger():
    log_format = (
        '{time:YYYY-MM-DD HH:mm:ss.SSSSSS} | '
        '<lvl>{level: ^9}</lvl> | '
        '{message}'
    )
    logger.add(sys.stderr, level='INFO', format=log_format)
    logger.add(
        f'./logs/algs.log',
        rotation='7 day',
        retention='30 days',
        level='INFO',
        encoding='UTF-8',
        format=log_format
    )

if __name__ == '__main__':
    set_logger()
    ALGSFan(logfile=logger).run()
