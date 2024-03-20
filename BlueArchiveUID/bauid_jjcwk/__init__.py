from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .bajjc_wk import bajjc_rank_to_pyroxene

sv_ba_jjcwk = SV('BA竞技场挖矿')


@sv_ba_jjcwk.on_command(('jjc挖矿', 'JJC挖矿'))
async def send_jjcwk_msg(bot: Bot, ev: Event):
    if not ev.text:
        await bot.send(
            '输入 赛季n 最高n（可省略汉字数字间留空格）\n'
            '输入示例：“赛季12 最高3”或“12 3”\n'
            '可省略最高名次，默认历史第一挖完\n'
            '输入示例：“赛季12”或“12”'
        )
    else:
        py = '剩余可挖青辉石' + bajjc_rank_to_pyroxene(ev.text)
        await bot.send(py)
