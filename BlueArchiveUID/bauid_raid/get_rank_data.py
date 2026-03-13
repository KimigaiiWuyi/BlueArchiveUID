import datetime
from typing import Union

from ..utils.ba_api import ba_api, xtzx_api
from ..utils.ba_config import ba_config

now_season = 7

SERVER_MAP = {"1": "官服", "2": "B服"}


async def get_ranking_from_xtzx(season: Union[str, int, None] = None, server_id: Union[str, int] = 1):
    sdata = await xtzx_api.get_now_season_data()
    if sdata is None:
        return "获取数据失败!"
    season = sdata["season"]
    title = f"~「第{season}期：{sdata['map']['value']} - {sdata['boss']}」~"

    server_id = str(server_id)
    im_list = [title]
    last_update = ""
    # for server_id in ['1', '2']:
    im_list.append(f"【{SERVER_MAP[server_id]}数据】:")
    data = await xtzx_api.get_xtzx_raid_chart(season, server_id)
    top_data = await xtzx_api.get_xtzx_raid_top(season, server_id)
    person_data = await xtzx_api.get_xtzx_raid_chart_person(season, server_id)
    person_rank_data = await xtzx_api.get_xtzx_raid_person(season, server_id)

    if person_data is not None:
        if person_data["value"] is not None:
            person_num = person_data["value"][-1]
            im_list.append(f"参与总人数: {person_num:,}")
        else:
            im_list.append("参与总人数: 未知")

    if person_rank_data is not None:
        if len(person_rank_data) >= 1:
            _num = None
            for i in person_rank_data[:2]:
                num = i["rank"] if _num is None else i["rank"] - _num
                im_list.append(f"{i['hard']}人数: {num}")
                _num = i["rank"] if _num is None else _num + i["rank"]

    if top_data is not None:
        for ix, i in enumerate(["🥇", "🥈", "🥉"]):
            if len(top_data) > ix:
                im_list.append(
                    f"{i}档线: {top_data[ix]['bestRankingPoint']:,}"
                    f"({top_data[ix]['hard']} - {top_data[ix]['battleTime']})"
                )

    if data is not None:
        _last_update = data["time"][-1]
        current_date = datetime.datetime.fromtimestamp(_last_update / 1000)
        last_update = current_date.strftime("%Y-%m-%d %H:%M:%S")
        for rank in [
            "1",
            "1000",
            "2000",
            "4000",
            "8000",
            "12000",
            "20000",
            "50000",
            "100000",
            "120000",
            "200000",
        ]:
            if rank in data["data"] and data["data"][rank] and data["data"][rank][-1]:
                im_list.append(f"第{rank}名: {data['data'][rank][-1]:,}")

    # im_list.append('✅换源请发【总力战档位】')
    if server_id == "1":
        im_list.append("✅查B服请发【ba总力战b】")
    else:
        im_list.append("✅查官服请发【ba总力战】")

    disable_xtzx_url: bool = ba_config.get_config("disable_xtzx_url").data

    if disable_xtzx_url:
        im_list.append("✅数据来源 什亭之匣(Arona ICU)")
    else:
        im_list.append("✅数据来源https://arona.icu/")

    im_list.append(f"✅最后更新于: {last_update}")

    return "\n".join(im_list)


async def get_ranking(season: Union[str, int, None] = now_season) -> str:
    if season is None:
        season = now_season

    data = await ba_api.get_raid_ranking(season)
    if data is None:
        return "获取数据失败!"

    ex_finished = data["exFinished"]
    bili_ex_finished = data["exFinished_bilibili"]
    _last_update = data["lastUpdatedTime"]
    current_date = datetime.datetime.fromtimestamp(_last_update)
    last_update = current_date.strftime("%Y-%m-%d %H:%M:%S")

    rank = {"官": {}, "B": {}}
    for title in ["data", "data_bilibili"]:
        for index in data[title]:
            for item in reversed(data[title][index]):
                if item[1]:
                    if title == "data":
                        rank["官"][f"{index}"] = item[1]
                    else:
                        rank["B"][f"{index}"] = item[1]
                    break

    im_list = []
    for t in rank:
        im_list.append(f"{t}服:")
        for d in rank[t]:
            im_list.append(f"第{d}名: {rank[t][d]:,}")

    im_list.append(f"官服Ex通过人数: {ex_finished}")
    im_list.append(f"B服Ex通过人数: {bili_ex_finished}")
    im_list.append(f"数据最后更新于: {last_update}")

    return "\n".join(im_list)
