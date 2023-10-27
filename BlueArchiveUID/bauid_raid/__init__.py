import re

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .get_rank_data import get_ranking, get_ranking_from_xtzx

sv_ba_raid = SV('BA总力战')


@sv_ba_raid.on_command(('总力战档位'))
async def send_raid_msg(bot: Bot, ev: Event):
    match = re.search(r'\d+', ev.text)
    season = match.group() if match else None
    await bot.send(await get_ranking(season))


@sv_ba_raid.on_command(('ba总力战', 'BA总力战'))
async def send_xtzx_msg(bot: Bot, ev: Event):
    match = re.search(r'\d+', ev.text)
    season = match.group() if match else None
    await bot.send(await get_ranking_from_xtzx(season))
