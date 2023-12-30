from gsuid_core.utils.download_resource.download_core import download_all_file

from .resource_path import HEHEDI_CHAR_GUIDE_PATH, HEHEDI_LEVEL_GUIDE_PATH


async def download_ba_resource():
    await download_all_file(
        'BlueArchiveUID',
        {
            'hehedi_level_guide': HEHEDI_LEVEL_GUIDE_PATH,
            'hehedi_char_guide': HEHEDI_CHAR_GUIDE_PATH,
        },
    )
