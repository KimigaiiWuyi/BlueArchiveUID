from pathlib import Path

from PIL import Image

path = Path(__file__).parent
CPATH = path / 'all_image'

CPATH.mkdir(exist_ok=True)

path_list = [i for i in path.rglob("*.png")]

for i in path_list:
    if '小春版' in i.stem:
        continue

    for b in path_list:
        if i.stem in b.stem and '小春' in b.stem:
            xcpath = b
            break
    else:
        print(f'{i} 没有找到对应的小春版')
        continue

    img1 = Image.open(i).convert('RGBA')
    img2 = Image.open(xcpath).convert('RGBA')

    img1_h = (1900 * img1.size[1]) / img1.size[0]
    img1 = img1.resize((1900, int(img1_h)))

    img2_h = (1900 * img2.size[1]) / img2.size[0]
    img2 = img2.resize((1900, int(img2_h)))

    img = Image.new(
        'RGB',
        (1900, int(img1_h + img2_h + 90)),
        color=(255, 255, 255),
    )

    img.paste(img1, (0, 30), img1)
    img.paste(img2, (0, int(img1_h + 60)), img2)

    img.save(CPATH / f"{i.stem}.jpg", format='JPEG', quality=95)
    print(f'{i} 合成完成')
