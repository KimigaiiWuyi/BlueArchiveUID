from typing import Any, Dict, List, Union, Literal, Optional

from gsuid_core.logger import logger
from aiohttp import FormData, TCPConnector, ClientSession, ContentTypeError

from ..ba_config import ba_config
from .api import (
    ARONA_URL,
    BATTLE_URL,
    XTZX_RAID_TOP,
    XTZX_RAID_LIST,
    XTZX_RAID_RANK,
    XTZX_RAID_CHART,
)

TOKEN = ba_config.get_config('xtzx_token').data

if not TOKEN:
    logger.warning('[BaUID] 如未配置 什亭之匣Token , ba总力战相关功能将无法正常使用')


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
        method: Literal["GET", "POST"] = "GET",
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
                    raw_data = {"retcode": -999, "data": _raw_data}
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
            season = now_season['season']
        data = await self._ba_request(XTZX_RAID_TOP.format(server_id, season))
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
            season = now_season['season']
        data = await self._ba_request(XTZX_RAID_RANK.format(server_id, season))
        if isinstance(data, Dict) and 'code' in data and data['code'] == 200:
            return data

    async def _ba_request(
        self,
        url: str,
        method: Literal["GET", "POST"] = "GET",
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
                    raw_data = {"retcode": -999, "data": _raw_data}
                logger.debug(raw_data)
                return raw_data
