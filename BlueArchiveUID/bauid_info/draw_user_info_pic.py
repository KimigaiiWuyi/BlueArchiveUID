from pathlib import Path
from typing import Union

from PIL import Image, ImageDraw
from gsuid_core.models import Event
from gsuid_core.utils.image.convert import convert_img
from gsuid_core.utils.fonts.fonts import core_font as cf
from gsuid_core.utils.image.image_tools import (
    crop_center_img,
    get_event_avatar,
    draw_pic_with_ring,
)

from ..utils.ba_api import xtzx_api
from ..utils.error_reply import get_error
from ..utils.resource_path import (
    SKILL_ICON_PATH,
    WEAPON_ICON_PATH,
    EQUIPMENT_ICON_PATH,
    STUDENT_COLLECTION_PATH,
)
from ..utils.ba_map import (
    equipId2Icon,
    weaponId2Nmae,
    studentId2Name,
    studentId2Type,
    studentSkill2Icon,
    studentId2weaponIcon,
)

TEXT_PATH = Path(__file__).parent / 'texture2d'
BLACK = (37, 37, 37)
GREY = (95, 102, 110)
weapon_star_full = Image.open(TEXT_PATH / 'weapon_star_full.png')
weapon_star_empty = Image.open(TEXT_PATH / 'weapon_star_empty.png')
footer = Image.open(TEXT_PATH / 'footer.png')

COLOR_MAP = {
    'explosion': (144, 1, 8),
    'pierce': (218, 160, 39),
    'mystic': (34, 111, 155),
    'sonic': (103, 79, 167),
}


async def draw_user_info_img(
    _fcode: str, ev: Event, user_id: str
) -> Union[str, bytes]:
    fcode, server = _fcode.split(':')
    data = await xtzx_api.get_xtzx_friend_data(fcode, server)

    if isinstance(data, int):
        return get_error(data)

    w, h = 1100, 2880
    img = crop_center_img(Image.open(TEXT_PATH / 'bg.jpg'), w, h)
    img = img.convert('RGBA')

    title = Image.open(TEXT_PATH / 'title.png')
    title_draw = ImageDraw.Draw(title)
    avatar = await get_event_avatar(ev)
    avatar = await draw_pic_with_ring(avatar, 308)
    title.paste(avatar, (396, 57), avatar)
    title_draw.text((550, 432), f'UserID: {user_id}', BLACK, cf(30), 'mm')

    img.paste(title, (0, 0), title)

    bar1 = Image.open(TEXT_PATH / 'bar.png')
    bar2 = Image.open(TEXT_PATH / 'bar.png')
    bar3 = Image.open(TEXT_PATH / 'bar.png')
    bar1draw = ImageDraw.Draw(bar1)
    bar2draw = ImageDraw.Draw(bar2)
    bar3draw = ImageDraw.Draw(bar3)
    bar1draw.text((550, 40), '基本信息', BLACK, cf(34), 'mm')
    bar2draw.text((550, 40), '总力助战', BLACK, cf(34), 'mm')
    bar3draw.text((550, 40), '演习助战', BLACK, cf(34), 'mm')

    img.paste(bar1, (0, 475), bar1)
    img.paste(bar2, (0, 865), bar2)
    img.paste(bar3, (0, 1845), bar3)

    avatar_card = Image.open(TEXT_PATH / 'avatar_card.png')

    game_avatar_id = data['representCharacterUniqueId']
    avatar_path = STUDENT_COLLECTION_PATH / f'{game_avatar_id}.webp'
    game_avatar = Image.open(avatar_path).convert('RGBA')

    game_nickname = data['nickname']
    game_comment = data['comment']
    game_level = str(data['level'])
    friend_count = str(data['friendCount'])
    count_str = f'好友数 {friend_count}/30'

    avatar_card_draw = ImageDraw.Draw(avatar_card)
    avatar_card.paste(game_avatar, (58, 87), game_avatar)

    avatar_card_draw.text((308, 177), game_nickname, GREY, cf(44), 'lm')
    avatar_card_draw.text((308, 284), game_comment, GREY, cf(28), 'lm')

    avatar_card_draw.text((497, 118), count_str, BLACK, cf(25), 'mm')
    avatar_card_draw.text((669, 118), f'{fcode}', BLACK, cf(25), 'mm')
    avatar_card_draw.text((816, 118), f'等级{game_level}', BLACK, cf(25), 'mm')

    img.paste(avatar_card, (0, 491), avatar_card)

    assist_list = data['assistInfoList']

    _assist_list = []
    for i in assist_list:
        if i['echelonType'] == 2:
            _assist_list.append(i)
    else:
        while len(_assist_list) < 2:
            _assist_list.append({})
        for i in assist_list:
            if i['echelonType'] == 15:
                _assist_list.append(i)
        else:
            while len(_assist_list) < 4:
                _assist_list.append({})

    for index, assist in enumerate(_assist_list):
        assist_card = Image.open(TEXT_PATH / 'assist_bg.png')
        if assist:
            assist_draw = ImageDraw.Draw(assist_card)

            student_id = assist['uniqueId']
            student_star = assist['starGrade']
            student_level = assist['level']
            student_star_pic = Image.open(
                TEXT_PATH / f'star{student_star}.png'
            )
            student_star_pic = student_star_pic.convert('RGBA')
            student_name = studentId2Name[str(student_id)]
            student_type = studentId2Type[str(student_id)]

            student_pic = Image.open(
                STUDENT_COLLECTION_PATH / f'{student_id}.webp'
            )
            student_color = COLOR_MAP[student_type]
            student_color_pic = Image.new(
                'RGBA', student_pic.size, student_color
            )

            favor_rank = assist['favorRank']
            ex = assist['exSkillLevel']
            nm = assist['publicSkillLevel']
            ps = assist['passiveSkillLevel']
            sub = assist['extraPassiveSkillLevel']

            skill_data = {
                'ex': ex,
                'nm': nm,
                'ps': ps,
                'sub': sub,
            }
            for sindex, s in enumerate(skill_data):
                skill_bg = Image.open(
                    TEXT_PATH / f'{student_type}_skill_bg.png'
                )
                skill_draw = ImageDraw.Draw(skill_bg)

                skill_icon = studentSkill2Icon[str(student_id)][s]
                skill_path = SKILL_ICON_PATH / f'{skill_icon}.webp'
                skill_pic = Image.open(skill_path).resize((36, 38))

                skill = skill_data[s] if skill_data[s] != 10 else 'M'
                skill_bg.paste(skill_pic, (25, 21), skill_pic)
                skill_draw.text((71, 40), f'等级{skill}', GREY, cf(34), 'lm')
                assist_card.paste(skill_bg, (312 + 172 * sindex, 96), skill_bg)

            assist_card.paste(student_color_pic, (66, 108), student_pic)
            assist_card.paste(student_pic, (68, 96), student_pic)
            assist_card.paste(student_star_pic, (228, 390), student_star_pic)
            assist_draw.text((146, 364), student_name, GREY, cf(32), 'mm')
            assist_draw.text(
                (251, 361), str(favor_rank), 'white', cf(25), 'mm'
            )
            assist_draw.text(
                (151, 414), f'等级{student_level}', BLACK, cf(25), 'mm'
            )

            weapon_bg = Image.open(TEXT_PATH / 'weapon_bar.png')
            if assist['weapon']:
                weapon_draw = ImageDraw.Draw(weapon_bg)

                weapon_star = assist['weaponStartGrade']
                weapon_name = weaponId2Nmae[str(student_id)]
                weapon_level = assist['weaponLevel']
                weapon_icon_id = studentId2weaponIcon[str(student_id)]
                weapon_path = WEAPON_ICON_PATH / f'{weapon_icon_id}.webp'
                weapon_icon = Image.open(weapon_path).resize((400, 102))

                weapon_bg.paste(weapon_icon, (11, 42), weapon_icon)
                weapon_draw.text(
                    (470, 70), f'等级{weapon_level}', BLACK, cf(25), 'mm'
                )
                weapon_draw.text((486, 115), weapon_name, BLACK, cf(38), 'lm')

                for i in range(5):
                    if i < weapon_star:
                        star_pic = weapon_star_full
                    else:
                        star_pic = weapon_star_empty
                    weapon_bg.paste(star_pic, (227 + 29 * i, 110), star_pic)

            assist_card.paste(weapon_bg, (275, 147), weapon_bg)

            equip_fg = Image.open(TEXT_PATH / 'equip_fg.png')
            for eindex, equip in enumerate(assist['equipment']):
                equip_bg = Image.open(TEXT_PATH / 'equip_bg.png')
                equip_id = equip['UniqueId']
                equip_icon = equipId2Icon[str(equip_id)]
                equip_pic = Image.open(
                    EQUIPMENT_ICON_PATH / f'{equip_icon}.webp'
                )
                equip_level = equip['Level']
                # equip_tier = equip['Tier']

                equip_bg.paste(equip_pic, (2, 17), equip_pic)
                equip_bg.paste(equip_fg, (0, 0), equip_fg)
                equip_bg_draw = ImageDraw.Draw(equip_bg)
                equip_bg_draw.text(
                    (75, 124),
                    f'等级{equip_level}',
                    'white',
                    cf(24),
                    'mm',
                )
                assist_card.paste(
                    equip_bg, (304 + eindex * 131, 306), equip_bg
                )

        x = 80 if index >= 2 else 0
        img.paste(assist_card, (0, 884 + 450 * index + x), assist_card)

    img.paste(footer, (0, h - 50), footer)
    im = await convert_img(img)

    return im
