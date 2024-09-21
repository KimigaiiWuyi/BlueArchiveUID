from pathlib import Path
from typing import Dict, Union

import aiofiles
from PIL import Image
from msgspec import json as msgjson
from gsuid_core.help.model import PluginHelp
from gsuid_core.utils.fonts.fonts import core_font
from gsuid_core.help.draw_plugin_help import get_help

from ..version import BlueArchiveUID_version

ICON = Path(__file__).parent.parent.parent / 'ICON.png'
TEXT_PATH = Path(__file__).parent / 'texture2d'
HELP_DATA = Path(__file__).parent / 'Help.json'


async def get_help_data() -> Union[Dict[str, PluginHelp], None]:
    if HELP_DATA.exists():
        async with aiofiles.open(HELP_DATA, 'rb') as file:
            return msgjson.decode(
                await file.read(),
                type=Dict[str, PluginHelp],
            )


async def get_ba_core_help() -> Union[bytes, str]:
    help_data = await get_help_data()
    if help_data is None:
        return '暂未找到帮助数据...'

    img = await get_help(
        'BlueArchiveUID',
        f'版本号:{BlueArchiveUID_version}',
        help_data,
        Image.open(TEXT_PATH / 'bg.jpg'),
        Image.open(TEXT_PATH / 'icon.png'),
        Image.open(TEXT_PATH / 'badge.png'),
        Image.open(TEXT_PATH / 'banner.png'),
        Image.open(TEXT_PATH / 'button.png'),
        core_font,
        is_dark=False,
        column=4,
        is_gaussian=True,
        gaussian_blur=10,
        text_color=(39, 87, 168),
        sub_c=(68, 128, 230),
        sv_color=(8, 8, 8),
        sv_desc_color=(58, 58, 58),
    )
    return img
