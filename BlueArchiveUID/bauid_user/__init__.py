from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.utils.message import send_diff_msg

from ..utils.database.models import BaBind

ba_user_bind = SV('ba用户绑定')


@ba_user_bind.on_command(
    (
        '绑定uid',
        '绑定UID',
        '绑定',
        '好友码',
        '切换uid',
        '切换UID',
        '切换',
        '删除uid',
        '删除UID',
        '删除',
    ),
    block=True,
)
async def send_ba_bind_uid_msg(bot: Bot, ev: Event):
    uid = (
        ev.text.strip()
        .replace('：', ':')
        .replace('好友', '')
        .replace('码', '')
    )

    if not uid:
        return await bot.send('该命令需要带上正确的好友码!')

    if ':' not in uid or not uid.endswith(('1', '2')):
        return await bot.send(
            '好友码需在末尾携带:符号以确认服务器\n:1为官服，:2为b服\n例如ba绑定vlhy4mw:1即为绑定官服vlhy4mw好友码'
        )

    await bot.logger.info('[Ba] 开始执行[绑定/解绑用户信息]')
    qid = ev.user_id
    await bot.logger.info('[Ba] [绑定/解绑]UserID: {}'.format(qid))

    if '绑定' in ev.command:
        data = await BaBind.insert_uid(
            qid, ev.bot_id, uid, ev.group_id, is_digit=False
        )
        return await send_diff_msg(
            bot,
            data,
            {
                0: f'[Ba] 绑定好友码{uid}成功！如绑定错误需删除，请使用命令：ba删除好友码',
                -1: f'[Ba] 好友码{uid}的位数不正确！',
                -2: f'[Ba] 好友码{uid}已经绑定过了！',
                -3: '[Ba] 你输入了错误的格式!',
            },
        )
    elif '切换' in ev.command:
        retcode = await BaBind.switch_uid_by_game(qid, ev.bot_id, uid)
        if retcode == 0:
            return await bot.send(f'[Ba] 切换好友码{uid}成功！')
        else:
            return await bot.send(f'[Ba] 尚未绑定该好友码{uid}')
    else:
        data = await BaBind.delete_uid(qid, ev.bot_id, uid)
        return await send_diff_msg(
            bot,
            data,
            {
                0: f'[Ba] 删除好友码{uid}成功！',
                -1: f'[Ba] 该好友码{uid}不在已绑定列表中！',
            },
        )
