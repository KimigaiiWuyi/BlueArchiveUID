from pathlib import Path

from gsuid_core.data_store import get_res_path

BG_PATH = Path(__file__).parent / 'bg'
MAIN_PATH = get_res_path('BlueArchiveUID')
GUIDE_PATH = MAIN_PATH / 'guide'
EVENT_PATH = MAIN_PATH / 'event'
CHAR_PATH = MAIN_PATH / 'char'
HEHEDI_LEVEL_GUIDE_PATH = MAIN_PATH / 'hehedi_level_guide'
HEHEDI_CHAR_GUIDE_PATH = MAIN_PATH / 'hehedi_char_guide'

RESOURCE_PATH = MAIN_PATH / 'resource'
EQUIPMENT_ICON_PATH = RESOURCE_PATH / 'equipment_icon'
SKILL_ICON_PATH = RESOURCE_PATH / 'skill_icon'
STUDENT_COLLECTION_PATH = RESOURCE_PATH / 'student_collection'
WEAPON_ICON_PATH = RESOURCE_PATH / 'weapon_icon'


def init_dir():
    for i in [
        MAIN_PATH,
        GUIDE_PATH,
        EVENT_PATH,
        CHAR_PATH,
        HEHEDI_LEVEL_GUIDE_PATH,
        HEHEDI_CHAR_GUIDE_PATH,
        RESOURCE_PATH,
        EQUIPMENT_ICON_PATH,
        SKILL_ICON_PATH,
        STUDENT_COLLECTION_PATH,
        WEAPON_ICON_PATH,
    ]:
        i.mkdir(parents=True, exist_ok=True)


init_dir()
