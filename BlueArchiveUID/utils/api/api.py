SOME_URL = 'https://arona.cdn.diyigemt.com/image'
GUIDE_URL = SOME_URL + '/chapter_map/{}.png'
ARONA_URL = 'https://arona.diyigemt.com/api/v1/image?name={}'

GAMERHUB_URL = 'http://ba.gamerhub.cn/api'
BATTLE_URL = (
    GAMERHUB_URL
    + '/get_ba_raid_ranking_data?season={}&ranking=1,2001,20001,30001'
)

XTZX_API = 'https://api.arona.icu'
XTZX_RAID_LIST = XTZX_API + '/api/season/list'
XTZX_RAID_RANK = XTZX_API + '/api/v2/rank/list'
XTZX_RAID_TOP = XTZX_API + '/api/v2/rank/list_top'
XTZX_RAID_CHART_PERSON = XTZX_API + '/api/v2/rank/season/lastRank/charts'
XTZX_RAID_CHART = XTZX_API + '/raid/new/charts/{}?s={}'
