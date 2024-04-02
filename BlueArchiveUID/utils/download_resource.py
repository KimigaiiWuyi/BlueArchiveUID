from gsuid_core.utils.download_resource.download_core import download_all_file

from .resource_path import (
    SKILL_ICON_PATH,
    WEAPON_ICON_PATH,
    EQUIPMENT_ICON_PATH,
    HEHEDI_CHAR_GUIDE_PATH,
    HEHEDI_LEVEL_GUIDE_PATH,
    STUDENT_COLLECTION_PATH,
)


async def download_ba_resource():
    await download_all_file(
        'BlueArchiveUID',
        {
            'hehedi_level_guide': HEHEDI_LEVEL_GUIDE_PATH,
            'hehedi_char_guide': HEHEDI_CHAR_GUIDE_PATH,
            'resource/equipment_icon': EQUIPMENT_ICON_PATH,
            'resource/weapon_icon': WEAPON_ICON_PATH,
            'resource/skill_icon': SKILL_ICON_PATH,
            'resource/student_collection': STUDENT_COLLECTION_PATH,
        },
    )
