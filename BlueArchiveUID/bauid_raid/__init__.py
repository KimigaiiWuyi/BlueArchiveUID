from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .get_rank_data import get_ranking

sv_ba_raid = SV('BA攻略')


@sv_ba_raid.on_fullmatch(('总力战档位', 'ba总力战'))
async def send_event_guide_pic(bot: Bot, ev: Event):
    await bot.send(await get_ranking())
