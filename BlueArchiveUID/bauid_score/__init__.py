from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .bata_score_to_time import bata_score_time
from .bata_rtime_to_score import bata_rtime_score
from .bata_utime_to_socre import bata_utime_score

sv_ba_score = SV('BA总力战算分')
sv_ba_time = SV('BA总力战算用时')


@sv_ba_score.on_command(('ba算分', 'BA算分'))
async def send_score_msg(bot: Bot, ev: Event):
    if not ev.text:
        await bot.send(
            '输入 难度+Boss+剩/用+分:秒.毫秒 算总力战分数\n'
            '支持省略分钟，支持省略毫秒，无符号默认为秒\n'
            '支持多刀计算，多个时间用空格间隔\n'
            '输入示例：ex寿司剩/用1:23.333 45.666 1:23 45'
        )
    else:
        if '剩' in ev.text:
            sc = bata_rtime_score(ev.text.replace(' ', ''))
            await bot.send(sc)
        elif '用' in ev.text:
            sc = bata_utime_score(ev.text.replace(' ', ''))
            await bot.send(sc)
        else:
            await bot.send('是用时还是剩时？请重新发送指令')


@sv_ba_time.on_command(('ba用时', 'BA用时'))
async def send_time_msg(bot: Bot, ev: Event):
    if not ev.text:
        await bot.send(
            '输入 Boss+分数 算总力战用时，输入示例：寿司12345678\n支持用W/w/万跟在数字后表单位，输入示例：寿司1234w'
        )
    else:
        tm = bata_score_time(ev.text)
        await bot.send(tm)
