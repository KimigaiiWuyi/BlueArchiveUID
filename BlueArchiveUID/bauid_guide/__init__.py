from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

from .get_char import get_char_img
from .get_event import get_event_img
from .get_guide import get_guide_img

sv_ba_wiki = SV('BAWIKI')
sv_ba_guide = SV('BA攻略')


@sv_ba_wiki.on_prefix(('ba角色攻略', 'BA角色攻略'))
async def send_ba_char_pic(bot: Bot, ev: Event):
    await bot.send(await get_char_img(ev.text))


@sv_ba_guide.on_prefix(('ba攻略', 'BA攻略'))
async def send_ba_stage_pic(bot: Bot, ev: Event):
    await bot.send(await get_guide_img(ev.text))


@sv_ba_guide.on_fullmatch(('ba活动攻略', 'BA活动攻略'))
async def send_event_guide_pic(bot: Bot, ev: Event):
    await bot.send(await get_event_img())
