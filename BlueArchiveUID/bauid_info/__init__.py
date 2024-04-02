from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.utils.database.api import get_uid

from ..utils.database.models import BaBind
from .draw_user_info_pic import draw_user_info_img

ba_user_info = SV('ba用户信息')


@ba_user_info.on_command(('ba查询'), block=True)
async def send_ba_user_info(bot: Bot, ev: Event):
    fcode, user_id = await get_uid(
        bot, ev, BaBind, partten=r'[A-Za-z0-9:：]+', get_user_id=True
    )

    if not fcode:
        return await bot.send(
            '未绑定好友码, 请先使用[ba绑定vlhy4mw]绑定好友码...\n如需临时查询，请使用[ba查询vlhy4mw:1]'
        )

    fcode = fcode.replace('：', ':')

    if ':' not in fcode or not fcode.endswith(('1', '2')):
        return await bot.send(
            '好友码需在末尾携带:符号以确认服务器\n:1为官服，:2为b服\n例如ba查询vlhy4mw:1即为查询官服vlhy4mw好友码'
        )

    im = await draw_user_info_img(fcode, ev, user_id)
    await bot.send(im)
