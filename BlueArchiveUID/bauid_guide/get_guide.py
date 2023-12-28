from typing import Union

from PIL import Image
from gsuid_core.utils.image.convert import convert_img

from ..utils.api.api import GUIDE_URL
from ..utils.ba_config import ba_config
from ..utils.download import download_file
from ..utils.resource_path import GUIDE_PATH, HEHEDI_GUIDE_PATH

guide_source = ba_config.get_config('guide_source').data


async def get_guide_img(battle: str) -> Union[bytes, str]:
    battle = (
        battle.strip()
        .replace('困难', 'H')
        .replace('Hard', 'H')
        .replace('h', 'H')
    )
    if battle.endswith('H'):
        battle = 'H' + battle[:-1]

    img = None
    path = HEHEDI_GUIDE_PATH / f'{battle}.jpg'
    if guide_source == 'hehedi' and path.exists():
        img = Image.open(path)
    elif guide_source == 'bawiki':
        img = await download_file(
            GUIDE_URL.format(battle), GUIDE_PATH, f'{battle}.png'
        )

    if img is None and path.exists():
        img = Image.open(path)
    elif img is None and not path.exists():
        img = await download_file(
            GUIDE_URL.format(battle), GUIDE_PATH, f'{battle}.png'
        )

    if isinstance(img, Image.Image):
        return await convert_img(img)

    return '未找到该BA攻略...'
