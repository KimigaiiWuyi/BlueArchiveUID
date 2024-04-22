from typing import Any, Dict, List, Union, Literal, Optional, cast

from gsuid_core.logger import logger
from aiohttp import FormData, TCPConnector, ClientSession, ContentTypeError

from ..ba_config import ba_config
from .models import DataItem, RankResp, FriendData
from .api import (
    ARONA_URL,
    BATTLE_URL,
    XTZX_RAID_TOP,
    XTZX_FIND_RANK,
    XTZX_RAID_LIST,
    XTZX_RAID_RANK,
    XTZX_RAID_CHART,
    XTZX_FRIEND_DATA,
    XTZX_FRIEND_RANK,
    XTZX_RAID_RANK_PERSON,
    XTZX_RAID_CHART_PERSON,
)

TOKEN = ba_config.get_config('xtzx_token').data

if not TOKEN:
    logger.warning(
        '[BaUID] 如未配置 什亭之匣Token , ba总力战相关功能将无法正常使用'
    )


class BaseBAApi:
    ssl_verify = True
    _HEADER: Dict[str, str] = {'Authorization': 'N'}

    async def get_arona_guide_index(self, name: str) -> Union[Dict, int]:
        return await self._ba_request(ARONA_URL.format(name.strip()))

    async def get_raid_ranking(
        self, season: Union[str, int]
    ) -> Optional[Dict]:
        data = await self._ba_request(BATTLE_URL.format(season))
        if isinstance(data, Dict) and 'errno' in data and data['errno'] == 0:
            return data

    async def _ba_request(
        self,
        url: str,
        method: Literal['GET', 'POST'] = 'GET',
        header: Dict[str, str] = _HEADER,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[FormData] = None,
    ) -> Union[Dict, int]:
        async with ClientSession(
            connector=TCPConnector(verify_ssl=self.ssl_verify)
        ) as client:
            async with client.request(
                method,
                url=url,
                headers=header,
                params=params,
                json=json,
                data=data,
                timeout=300,
            ) as resp:
                try:
                    raw_data = await resp.json()
                except ContentTypeError:
                    _raw_data = await resp.text()
                    raw_data = {'retcode': -999, 'data': _raw_data}
                logger.debug(raw_data)
                return raw_data


class XTZXApi(BaseBAApi):
    ssl_verify = True
    _HEADER = {'Authorization': f'ba-token {TOKEN}'}

    async def get_xtzx_raid_list(self) -> Optional[List[Dict]]:
        data = await self._ba_request(XTZX_RAID_LIST)
        if isinstance(data, Dict):
            return data['data']

    async def get_now_season_data(self) -> Optional[Dict]:
        data = await self.get_xtzx_raid_list()
        if data is None:
            return None
        return data[0]

    async def get_xtzx_raid_chart_person(
        self,
        season: Union[str, int, None] = None,
        server_id: Union[str, int] = 1,
    ) -> Optional[Dict]:
        if season is None:
            now_season = await self.get_now_season_data()
            if now_season is None:
                return None
            season = int(now_season['season'])
        data = await self._ba_request(
            XTZX_RAID_CHART_PERSON,
            'POST',
            json={
                'server': int(server_id),
                'season': int(season),
            },
        )
        if (
            isinstance(data, Dict)
            and 'data' in data
            and 'code' in data
            and data['code'] == 200
        ):
            return data['data']

    async def get_xtzx_raid_chart(
        self,
        season: Union[str, int, None] = None,
        server_id: Union[str, int] = 1,
    ) -> Optional[Dict]:
        if season is None:
            now_season = await self.get_now_season_data()
            if now_season is None:
                return None
            season = now_season['season']
        data = await self._ba_request(
            XTZX_RAID_CHART.format(server_id, season)
        )
        if (
            isinstance(data, Dict)
            and 'data' in data
            and 'code' in data
            and data['code'] == 200
        ):
            return data['data']

    async def get_xtzx_raid_top(
        self,
        season: Union[str, int, None] = None,
        server_id: Union[str, int] = 1,
    ) -> Optional[List[Dict]]:
        if season is None:
            now_season = await self.get_now_season_data()
            if now_season is None:
                return None
            season = int(now_season['season'])
        data = await self._ba_request(
            XTZX_RAID_TOP,
            'POST',
            json={'server': int(server_id), 'season': int(season)},
        )
        if (
            isinstance(data, Dict)
            and 'data' in data
            and 'code' in data
            and data['code'] == 200
        ):
            return data['data']

    async def get_xtzx_raid_ranking(
        self,
        season: Union[str, int, None] = None,
        server_id: Union[str, int] = 1,
    ):
        if season is None:
            now_season = await self.get_now_season_data()
            if now_season is None:
                return None
            season = int(now_season['season'])
        data = await self._ba_request(
            XTZX_RAID_RANK,
            'POST',
            json={
                'server': int(server_id),
                'season': int(season),
                'type': 2,
                'page': 1,
                'size': 26,
            },
        )
        if isinstance(data, Dict) and 'code' in data and data['code'] == 200:
            return data

    async def get_xtzx_raid_person(
        self,
        season: Union[str, int, None] = None,
        server_id: Union[str, int] = 1,
        data_type: int = 0,
        try_number: int = 0,
    ):
        if season is None:
            now_season = await self.get_now_season_data()
            if now_season is None:
                return None
            season = int(now_season['season'])
        data = await self._ba_request(
            XTZX_RAID_RANK_PERSON,
            'POST',
            json={
                'server': int(server_id),
                'season': int(season),
                "dataType": data_type,
                "tryNumber": try_number,
            },
        )
        if isinstance(data, Dict) and 'code' in data and data['code'] == 200:
            return cast(List[DataItem], data['data'])

    async def get_xtzx_friend_data(
        self,
        friend_code: str,
        server_id: Union[str, int] = 1,
    ) -> Union[int, FriendData]:
        data = await self._ba_request(
            XTZX_FRIEND_DATA,
            'POST',
            json={
                'server': int(server_id),
                'friend': friend_code,
            },
        )
        if isinstance(data, Dict) and 'code' in data:
            if data['code'] == 200:
                return cast(FriendData, data['data'])
            else:
                return data['code']
        else:
            return -500

    async def get_xtzx_find_rank(
        self,
        friend_code: str,
    ) -> Union[int, FriendData]:
        data = await self._ba_request(
            XTZX_FIND_RANK,
            'POST',
            json={
                'friend': friend_code,
            },
        )
        if isinstance(data, Dict) and 'code' in data:
            if data['code'] == 200:
                return cast(FriendData, data['data'])
            else:
                return data['code']
        else:
            return -500

    async def get_xtzx_friend_ranking(
        self,
        page: int,
        student_id: Union[str, int] = 10000,
    ) -> Union[int, RankResp]:
        data = await self._ba_request(
            XTZX_FRIEND_RANK,
            'POST',
            json={
                'page': page,
                'studentId': student_id,
            },
        )
        if isinstance(data, Dict) and 'code' in data:
            if data['code'] == 200:
                return cast(RankResp, data['data'])
            else:
                return data['code']
        else:
            return -500

    async def _ba_request(
        self,
        url: str,
        method: Literal['GET', 'POST'] = 'GET',
        header: Dict[str, str] = _HEADER,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[FormData] = None,
    ) -> Union[Dict, int]:
        if not TOKEN:
            logger.error('[BaUID] 未配置 什亭之匣Token , 无法使用ba总力战!')
            return -9999
        async with ClientSession(
            connector=TCPConnector(verify_ssl=self.ssl_verify)
        ) as client:
            async with client.request(
                method,
                url=url,
                headers=header,
                params=params,
                json=json,
                data=data,
                timeout=300,
            ) as resp:
                try:
                    raw_data = await resp.json()
                except ContentTypeError:
                    _raw_data = await resp.text()
                    raw_data = {'code': -999, 'data': _raw_data}
                logger.debug(raw_data)
                if 'code' in raw_data:
                    if raw_data['code'] != 0 and raw_data['code'] != 200:
                        logger.error(
                            f'[BaUID] 访问 {url} 失败, 错误码: {raw_data["retcode"]}'
                            f', 错误返回: {raw_data}'
                        )
                return raw_data
