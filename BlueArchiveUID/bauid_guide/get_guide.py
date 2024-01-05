from typing import List, Union

from PIL import Image
from gsuid_core.utils.image.convert import convert_img

from ..utils.api.api import GUIDE_URL
from ..utils.ba_config import ba_config
from ..utils.download import download_file
from ..utils.resource_path import GUIDE_PATH, HEHEDI_LEVEL_GUIDE_PATH

guide_source = ba_config.get_config('guide_source').data


async def get_guide_img(battle: str) -> Union[List[bytes], str]:
    battle = (
        battle.strip()
        .replace('困难', 'H')
        .replace('Hard', 'H')
        .replace('h', 'H')
    )
    if battle.endswith('H'):
        battle = 'H' + battle[:-1]

    path = HEHEDI_LEVEL_GUIDE_PATH / f'{battle}.jpg'

    img_list = []
    if (guide_source == 'hehedi' or guide_source == 'all') and path.exists():
        img_list.append(Image.open(path))

    if guide_source == 'bawiki' or not img_list or guide_source == 'all':
        img_list.append(
            await download_file(
                GUIDE_URL.format(battle), GUIDE_PATH, f'{battle}.png'
            )
        )

    if not img_list and path.exists():
        img_list.append(Image.open(path))

    if img_list:
        return [await convert_img(img) for img in img_list]

    return '未找到该BA攻略...'
