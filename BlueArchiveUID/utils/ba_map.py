from typing import Dict

from msgspec import json as msgjson

from ..tools.make_map import (
    equipId2Icon_path,
    weaponId2Nmae_path,
    studentId2Name_path,
    studentId2Type_path,
    studentSkill2Icon_path,
    studentId2weaponIcon_path,
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
