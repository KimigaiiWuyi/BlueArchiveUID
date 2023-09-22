from typing import Union

from PIL import Image
from gsuid_core.utils.image.convert import convert_img

from ..utils.api.api import GUIDE_URL
from ..utils.download import download_file
from ..utils.resource_path import GUIDE_PATH


async def get_guide_img(battle: str) -> Union[bytes, str]:
    battle = battle.strip().replace('困难', 'H').replace('Hard', 'H')
    if battle.endswith('H'):
        battle = 'H' + battle[:-1]
    img = await download_file(
        GUIDE_URL.format(battle), GUIDE_PATH, f'{battle}.png'
    )
    if isinstance(img, Image.Image):
        return await convert_img(img)

    return '未找到该BA攻略...'
