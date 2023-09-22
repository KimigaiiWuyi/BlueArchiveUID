from typing import Union

from PIL import Image
from gsuid_core.utils.image.convert import convert_img

from ..utils.ba_api import ba_api
from ..utils.api.api import SOME_URL
from ..utils.download import download_file
from ..utils.resource_path import CHAR_PATH


async def get_char_img(name: str) -> Union[bytes, str]:
    data = await ba_api.get_arona_guide_index(name)
    if isinstance(data, int):
        return '获取角色攻略失败...'

    if data['status'] == 101:
        name = data['data'][0]['name']
        data = await ba_api.get_arona_guide_index(name)
        if isinstance(data, int):
            return '获取角色攻略失败...'

    pic_name = data['data'][0]['hash']
    url = SOME_URL + data['data'][0]['path']
    img = await download_file(url, CHAR_PATH, f'{pic_name}.png')

    if isinstance(img, Image.Image):
        return await convert_img(img)

    return '获取角色攻略失败...'
