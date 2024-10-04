from typing import Dict
from pathlib import Path

import aiofiles
from PIL import Image
from msgspec import json as msgjson
from gsuid_core.help.model import PluginHelp
from gsuid_core.help.draw_new_plugin_help import get_new_help

from ..utils.image import get_footer
from ..version import BlueArchiveUID_version

ICON = Path(__file__).parent.parent.parent / 'ICON.png'
HELP_DATA = Path(__file__).parent / 'help.json'
ICON_PATH = Path(__file__).parent / 'icon_path'
TEXT_PATH = Path(__file__).parent / 'texture2d'


async def get_help_data() -> Dict[str, PluginHelp]:
    async with aiofiles.open(HELP_DATA, 'rb') as file:
        return msgjson.decode(await file.read(), type=Dict[str, PluginHelp])


async def get_help():
    return await get_new_help(
        plugin_name='BlueArchiveUID',
        plugin_info={f'v{BlueArchiveUID_version}': ''},
        plugin_icon=Image.open(ICON),
        plugin_help=await get_help_data(),
        plugin_prefix='ba',
        help_mode='light',
        banner_bg=Image.open(TEXT_PATH / 'banner_bg.jpg'),
        banner_sub_text='「与你的日常，就是“奇迹”」',
        help_bg=Image.open(TEXT_PATH / 'bg.jpg'),
        cag_bg=Image.open(TEXT_PATH / 'cag_bg.png'),
        item_bg=Image.open(TEXT_PATH / 'item.png'),
        icon_path=ICON_PATH,
        footer=get_footer(),
        enable_cache=True,
    )
