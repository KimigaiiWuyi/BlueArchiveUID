from typing import Optional

from PIL import Image
from gsuid_core.utils.image.convert import convert_img

from .alias import alias
from ..utils.ba_api import ba_api
from ..utils.api.api import SOME_URL
from ..utils.download import download_file
from ..utils.alias.name_convert import alias_to_char_name
from ..utils.resource_path import CHAR_PATH, HEHEDI_CHAR_GUIDE_PATH


async def get_hehedi_char_img(name: str) -> Optional[str]:
    name = alias_to_char_name(name)
    return await _get_hehedi_char_img(name)


async def _get_hehedi_char_img(name: str) -> Optional[str]:
    path = HEHEDI_CHAR_GUIDE_PATH / f'{name}.jpg'
    if path.exists():
        return await convert_img(path)
    return None


async def get_char_img(name: str) -> Optional[bytes]:
    for i in alias:
        if name in alias[i]:
            name = i
            break

    data = await ba_api.get_arona_guide_index(name)
    if isinstance(data, int):
        return None

    if data['status'] == 101:
        name = data['data'][0]['name']
        data = await ba_api.get_arona_guide_index(name)
        if isinstance(data, int):
            return None

    pic_name = data['data'][0]['hash']
    url = SOME_URL + data['data'][0]['path']
    img = await download_file(url, CHAR_PATH, f'{pic_name}.png')

    if isinstance(img, Image.Image):
        return await convert_img(img)

    return None
