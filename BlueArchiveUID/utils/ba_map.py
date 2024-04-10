from typing import Dict

from msgspec import json as msgjson

from .alias.name_convert import alias_to_char_name
from ..tools.make_map import (
    equipId2Icon_path,
    weaponId2Nmae_path,
    studentId2Name_path,
    studentId2Type_path,
    stageId2AreaNum_path,
    studentSkill2Icon_path,
    studentId2weaponIcon_path,
)

with open(stageId2AreaNum_path, 'r', encoding='UTF-8') as f:
    stageId2AreaNum = msgjson.decode(
        f.read(),
        type=Dict[str, str],
    )

with open(studentId2weaponIcon_path, 'r', encoding='UTF-8') as f:
    studentId2weaponIcon = msgjson.decode(
        f.read(),
        type=Dict[str, str],
    )

with open(studentId2Type_path, 'r', encoding='UTF-8') as f:
    studentId2Type = msgjson.decode(
        f.read(),
        type=Dict[str, str],
    )

with open(weaponId2Nmae_path, 'r', encoding='UTF-8') as f:
    weaponId2Nmae = msgjson.decode(
        f.read(),
        type=Dict[str, str],
    )

with open(equipId2Icon_path, 'r', encoding='UTF-8') as f:
    equipId2Icon = msgjson.decode(
        f.read(),
        type=Dict[str, str],
    )

with open(studentId2Name_path, 'r', encoding='UTF-8') as f:
    studentId2Name = msgjson.decode(
        f.read(),
        type=Dict[str, str],
    )

with open(studentSkill2Icon_path, 'r', encoding='UTF-8') as f:
    studentSkill2Icon = msgjson.decode(
        f.read(),
        type=Dict[str, Dict[str, str]],
    )


def student_name_to_id(name: str) -> str:
    name = alias_to_char_name(name)
    for _id in studentId2Name:
        if name in studentId2Name[_id]:
            return _id
    else:
        return '9999'
