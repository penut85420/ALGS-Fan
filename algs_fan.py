import os
import datetime as dt
from twitchio.ext import commands
from twsc_calendar import TWSCCalendar

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_NICK'],
            prefix='!',
            initial_channels=os.environ['CHANNEL'].split(',')
        )
        self.tc = TWSCCalendar()

    async def event_ready(self):
        print(f'{self.nick} is ready')

    async def event_message(self, msg):
        print(f'{msg.timestamp} [{msg.author.channel}] {msg.author.name}: {msg.content}')
        await self.handle_commands(msg)

    @commands.command(name='hello', aliases=['哈囉'])
    async def testing(self, ctx):
        await ctx.send(f'{ctx.author.name} 你好啊!')

    @commands.command(name='星海比賽', aliases=['日程', '比賽'])
    async def calendar(self, ctx):
        await ctx.send(self.tc.get_next_event())

    @commands.command(name='Nice', aliases=['nice'])
    async def nice(self, ctx):
        await ctx.send('死亡鳳凰艦隊提督 GivePLZ 亞細亞催銀神帝 GivePLZ')

if __name__ == '__main__':
    bot = Bot()
    bot.run()
