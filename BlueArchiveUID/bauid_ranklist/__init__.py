from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .draw_rank_pic import draw_rank_pic

sv_ba_xtzx_rank = SV('BA什亭之匣学生排行榜')


@sv_ba_xtzx_rank.on_command(
    (
        '学生排行',
        '学生排名',
        '角色排名',
        '角色排行',
    )
)
async def send_rank_msg(bot: Bot, ev: Event):
    await bot.send(await draw_rank_pic(ev.text.strip()))
