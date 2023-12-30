from pathlib import Path

from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img

sv_ba_ect = SV('BA杂图')

IMG_PATH = Path(__file__).parent / 'img'


@sv_ba_ect.on_fullmatch(('ba节奏榜', 'BA节奏榜', 'ba角色排行榜'))
async def send_charrank_guide_pic(bot: Bot, ev: Event):
    await bot.send(await convert_img(IMG_PATH / '国服节奏榜.jpg'))
