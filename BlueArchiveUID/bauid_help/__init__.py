from PIL import Image
from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.logger import logger
from gsuid_core.help.utils import register_help

from .get_help import ICON, get_ba_core_help

sv_ba_help = SV('BA帮助')


@sv_ba_help.on_fullmatch(('ba帮助', '蔚蓝档案帮助', 'BA帮助'))
async def send_help_img(bot: Bot, ev: Event):
    logger.info('开始执行[ba帮助]')
    im = await get_ba_core_help()
    await bot.send(im)


register_help('BlueArchiveUID', 'ba帮助', Image.open(ICON))
