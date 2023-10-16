import datetime
from typing import Union

from ..utils.ba_api import ba_api


async def get_ranking(season: Union[str, int] = 5) -> str:
    data = await ba_api.get_raid_ranking(season)
    if data is None:
        return '获取数据失败!'

    ex_finished = data['exFinished']
    bili_ex_finished = data['exFinished_bilibili']
    _last_update = data['lastUpdatedTime']
    current_date = datetime.datetime.fromtimestamp(_last_update)
    last_update = current_date.strftime('%Y-%m-%d %H:%M:%S')

    rank = {'官': {}, 'B': {}}
    for title in ['data', 'data_bilibili']:
        for index in data[title]:
            for item in reversed(data[title][index]):
                if item[1]:
                    if title == 'data':
                        rank['官'][f'{index}'] = item[1]
                    else:
                        rank['B'][f'{index}'] = item[1]
                    break

    im_list = []
    for t in rank:
        im_list.append(f'{t}服:')
        for d in rank[t]:
            im_list.append(f'第{d}名: {rank[t][d]}')

    im_list.append(f'官服Ex通过人数: {ex_finished}')
    im_list.append(f'B服Ex通过人数: {bili_ex_finished}')
    im_list.append(f'数据最后更新于: {last_update}')

    return '\n'.join(im_list)
