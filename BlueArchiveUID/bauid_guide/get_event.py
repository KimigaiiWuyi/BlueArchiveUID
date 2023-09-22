from typing import Union

from PIL import Image
from gsuid_core.utils.image.convert import convert_img

from ..utils.ba_api import ba_api
from ..utils.api.api import SOME_URL
from ..utils.download import download_file
from ..utils.resource_path import EVENT_PATH


async def get_event_img() -> Union[str, bytes]:
    data = await ba_api.get_arona_guide_index('国服活动')
    if isinstance(data, int):
        return '获取国服活动攻略失败...'

    pic_name = data['data'][0]['hash']
    url = SOME_URL + data['data'][0]['path']
    img = await download_file(url, EVENT_PATH, f'{pic_name}.png')

    if isinstance(img, Image.Image):
        return await convert_img(img)

    return '获取国服活动攻略失败...'
