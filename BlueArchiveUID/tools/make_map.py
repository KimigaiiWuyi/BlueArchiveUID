import json
from pathlib import Path
from typing import Any, Dict, List

from msgspec import json as msgjson

schale_db = Path(__file__).parent / 'SchaleDB'
MAP = Path(__file__).parents[1] / 'utils' / 'map'

student_data_path = schale_db / 'students.json'
equip_data_path = schale_db / 'equipment.json'
stages_data_path = schale_db / 'stages.json'

studentId2Name_path = MAP / 'studentId2Name_map.json'
studentId2Type_path = MAP / 'studentId2Type_map.json'
studentId2weaponIcon_path = MAP / 'studentId2weaponIcon_map.json'
equipId2Icon_path = MAP / 'equipId2Icon_map.json'
studentSkill2Icon_path = MAP / 'studentSkill2Icon_map.json'
weaponId2Nmae_path = MAP / 'weaponId2Nmae_map.json'
stageId2AreaNum_path = MAP / 'stageId2AreaNum_map.json'


def make_stageId2AreaNum():
    result = {}
    for stage in stages_data['Campaign']:
        a = f"{stage['Area']}-{stage['Stage']}"
        if stage['Difficulty'] > 0:
            a += 'H'
        result[stage['Id']] = a
    with open(stageId2AreaNum_path, 'w', encoding='UTF-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


def make_id2name():
    result = {}
    result2 = {}
    result3 = {}

    for student in student_data:
        result[student['Id']] = student['FamilyName'] + student['PersonalName']
        result2[student['Id']] = student['BulletType'].lower()
        result3[student['Id']] = student['WeaponImg']

    with open(studentId2Name_path, 'w', encoding='UTF-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    with open(studentId2Type_path, 'w', encoding='UTF-8') as f:
        json.dump(result2, f, indent=4, ensure_ascii=False)

    with open(studentId2weaponIcon_path, 'w', encoding='UTF-8') as f:
        json.dump(result3, f, indent=4, ensure_ascii=False)


def make_weaponId2Nmae():
    result = {}
    for student in student_data:
        result[student['Id']] = student['Weapon']['Name']
    with open(weaponId2Nmae_path, 'w', encoding='UTF-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


def make_equipId2Icon():
    result = {}
    for equip in equip_data:
        result[equip['Id']] = equip['Icon']
    with open(equipId2Icon_path, 'w', encoding='UTF-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


def make_studentSkill2Icon():
    result = {}
    for student in student_data:
        _r = {}
        skills = student['Skills']
        for skill in skills:
            if skill['SkillType'] == 'ex':
                _r['ex'] = skill['Icon']
            elif skill['SkillType'] == 'normal':
                _r['nm'] = skill['Icon']
            elif skill['SkillType'] == 'passive':
                _r['ps'] = skill['Icon']
            elif skill['SkillType'] == 'sub':
                _r['sub'] = skill['Icon']
        result[student['Id']] = _r
    with open(studentSkill2Icon_path, 'w', encoding='UTF-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


def make_map():
    make_id2name()
    make_equipId2Icon()
    make_studentSkill2Icon()
    make_weaponId2Nmae()
    make_stageId2AreaNum()


if __name__ == '__main__':
    with open(student_data_path, 'r', encoding='UTF-8') as f:
        student_data = msgjson.decode(
            f.read(),
            type=List[Dict[str, Any]],
        )

    with open(equip_data_path, 'r', encoding='UTF-8') as f:
        equip_data = msgjson.decode(
            f.read(),
            type=List[Dict[str, Any]],
        )

    with open(stages_data_path, 'r', encoding='UTF-8') as f:
        stages_data = msgjson.decode(
            f.read(),
            type=Dict[str, List[Dict[str, Any]]],
        )

    make_map()
