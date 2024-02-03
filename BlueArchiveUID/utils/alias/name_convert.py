import json
from pathlib import Path
from typing import Dict, List

ALIAS_PATH = Path(__file__).parent / "alias_data.json"

with open(ALIAS_PATH, 'r', encoding='utf8') as fp:
    alias_data: Dict[str, List] = json.loads(fp.read())

sp_version = {
    '泳装': ['泳', '泳装'],
    '私服': ['私', '私服'],
    '小': ['幼', '萝莉'],
    '单车': ['单车'],
    '正月': ['正月', '新春'],
}


def alias_to_char_name(char_name: str):
    char_name = (
        char_name.replace('（', '')
        .replace('(', '')
        .replace(')', '')
        .replace('）', '')
    )

    for sp in sp_version:
        for _sp in sp_version[sp]:
            if _sp in char_name:
                char_name = char_name.replace(_sp, '')
                char_name = char_name + f'_{sp}'
                break

    for i in alias_data:
        if (char_name in i) or (char_name in alias_data[i]):
            return i

    return char_name
