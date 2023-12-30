import json
from pathlib import Path

from PIL import Image

path = Path(__file__).parent
CPATH = path / 'all_image'

CPATH.mkdir(exist_ok=True)

path_list = [i for i in path.rglob("*.png")]
json_path = path / "result.json"

result = {}

for i in path_list:
    img = Image.open(i).convert('RGB')
    img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)))
    img.save(CPATH / f"{i.stem}.jpg", format='JPEG', quality=95)
    result[i.stem] = [i.stem]

with open(json_path, mode='w+', encoding='utf8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)
