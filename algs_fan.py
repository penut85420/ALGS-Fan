import os
import sys
import asyncio
import datetime as dt

from twitchio.ext import commands
from twitchio.ext.commands.errors import CommandNotFound
from twsc_calendar import TWSCCalendar

class ALGSFan(commands.Bot):
    def __init__(self, logfile=sys.stdout, verbose=True):
        self.logfile = logfile
        self.verbose = verbose
        super().__init__(
            irc_token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_NICK'],
            prefix='!',
            initial_channels=os.environ['CHANNEL'].split(',')
        )
        self.tc = TWSCCalendar()

    def log(self, msg):
        ts = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg = f'{ts} | {msg}\n'
        self.logfile.write(msg)
        self.logfile.flush()
        if self.verbose:
            sys.stdout.write(msg)

    async def event_ready(self):
        self.log(f'{self.nick} is ready')
        while True:
            for ch in self.initial_channels:
                ch = self.get_channel(ch)
                msg = self.tc.get_next_event()
                await ch.send(msg)
            await asyncio.sleep(1200)

    async def event_message(self, msg):
        self.log(f'[{msg.author.channel}] {msg.author.name}: {msg.content}')
        await self.handle_commands(msg)

    async def event_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            msg = f'Command "{ctx.content}" send from [{ctx.author.channel}] {ctx.author.name} was not found.'
            self.log(msg)
        else:
            self.log(str(error).replace('\n', ' | '))

    @commands.command(name='星海比賽', aliases=['日程', '比賽'])
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

    @commands.command(name='Nice', aliases=['nice'])
    async def nice(self, ctx):
        await ctx.send('死亡鳳凰艦隊提督 GivePLZ 抓放軍團最高統帥 GivePLZ 冰雪風暴靜滯領主 GivePLZ 亞細亞洲璀銀神帝 GivePLZ')

    @commands.command(name='阿吉')
    async def ahchi(self, ctx):
        await ctx.send('恭迎吉孤觀音⎝༼ ◕д ◕ ༽⎠ 渡世靈顯四方⎝༼ ◕д ◕ ༽⎠')

    @commands.command(name='Top', aliases=['top'])
    async def top(self, ctx):
        await ctx.send('吃我的大火球～～～')

    @commands.command(name='堅持')
    async def persist(self, ctx):
        await ctx.send('你在堅持啥啊')

    @commands.command(name='提告', aliases=['sue'])
    async def sue(self, ctx):
        await ctx.send('Nice：「不排除提告」（設計對白）')

    @commands.command(name='釣魚')
    async def fishing(self, ctx):
        await ctx.send('GivePLZ ／︴只有天選之人能釣到這條魚 _________________ SabaPing')

if __name__ == '__main__':
    logdir = './logs'
    os.makedirs(logdir, exist_ok=True)
    ts = dt.datetime.now().strftime('%Y%m%d.log')
    fn = os.path.join(logdir, ts)
    logfile = open(fn, 'a', encoding='UTF-8')

    ALGSFan(logfile=logfile).run()
