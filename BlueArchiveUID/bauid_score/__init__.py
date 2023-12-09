from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .bata_score_to_time import bata_time
from .bata_time_to_score import bata_score

sv_ba_score = SV('BA总力战算分')
sv_ba_time = SV('BA总力战算用时')


@sv_ba_score.on_command(('ba算分', 'BA算分'))
async def send_score_msg(bot: Bot, ev: Event):
    if not ev.text:
        await bot.send(
            '输入 难度+Boss+剩x:xx.xxx 算总力战分数，输入示例：ex寿司剩1:23.433\n'
            '请注意！分钟和秒用冒号分割！秒和毫秒用点分割！\n'
            '支持多刀计算，支持省略分钟，支持省略毫秒，只需空格+下一刀剩余时间，输入示例：ex寿司剩1:23.433 56.789 1:23'
        )
    else:
        sc = bata_score(ev.text)
        await bot.send(sc)


@sv_ba_time.on_command(('ba用时', 'BA用时'))
async def send_time_msg(bot: Bot, ev: Event):
    if not ev.text:
        await bot.send(
            '输入 Boss+分数 算总力战用时，输入示例：寿司12345678\n支持用W/w/万跟在数字后表单位，输入示例：寿司1234w'
        )
    else:
        tm = bata_time(ev.text)
        await bot.send(tm)
