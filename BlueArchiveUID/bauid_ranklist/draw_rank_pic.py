from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.fonts.fonts import core_font as cf

from ..utils.ba_api import xtzx_api
from ..utils.error_reply import get_error
from ..utils.ba_map import student_name_to_id
from ..bauid_info.draw_user_info_pic import BLACK, get_bg, draw_assist_card

TEXT_PATH = Path(__file__).parent / 'texture2d'


def get_color(rank_key: int):
    if rank_key < 10:
        rank_color = (235, 126, 163)
    elif rank_key < 80:
        rank_color = (235, 177, 129)
    elif rank_key < 200:
        rank_color = (151, 129, 235)
    else:
        rank_color = (202, 235, 129)
    return rank_color


async def draw_rank_pic(student: str) -> Union[bytes, str]:
    student_id = student_name_to_id(student)
    if student_id == '9999':
        return '要查询的角色不存在或别名未收录, 请尝试使用完整名字。'

    data = await xtzx_api.get_xtzx_friend_ranking(1, student_id)
    if isinstance(data, int):
        return get_error(data)
    teacher_data = data['records']

    img = get_bg(1100, 2800)
    for index, teacher in enumerate(teacher_data):
        info = teacher['assistInfoList'][0]
        rank_key = info['baRank']['key']
        rank_value = info['baRank']['value']
        rank_str = f'{rank_key} / {rank_value}'

        global_rank_key = info['baGlobalRank']['key']
        global_rank_value = info['baGlobalRank']['value']
        global_rank_str = f'{global_rank_key} / {global_rank_value}'

        rank_color = get_color(rank_key)
        global_rank_color = get_color(global_rank_key)

        card = Image.open(TEXT_PATH / 'card.png')

        card_draw = ImageDraw.Draw(card)

        card_draw.text(
            (230, 52),
            f'{teacher["nickname"]}',
            BLACK,
            cf(40),
            'lm',
        )

        if teacher['server'] == 1:
            s_f = (136, 205, 242)
            s_t = '官服'
        else:
            s_f = (243, 143, 225)
            s_t = 'B服'

        card_draw.rounded_rectangle((50, 36, 124, 68), 30, s_f)
        card_draw.text(
            (87, 52),
            s_t,
            BLACK,
            cf(24),
            'mm',
        )

        card_draw.rounded_rectangle((632, 36, 780, 68), 30, rank_color)
        card_draw.rounded_rectangle((904, 36, 1052, 68), 30, global_rank_color)
        card_draw.text(
            (706, 52),
            rank_str,
            BLACK,
            cf(24),
            'mm',
        )
        card_draw.text(
            (978, 52),
            global_rank_str,
            BLACK,
            cf(24),
            'mm',
        )
        assist_card = await draw_assist_card(info)

        img.paste(card, (0, 28 + index * 550), card)
        img.paste(assist_card, (0, 68 + index * 550), assist_card)

    img = await convert_img(img)
    return img
