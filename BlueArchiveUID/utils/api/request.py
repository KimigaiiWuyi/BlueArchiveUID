from typing import Any, Dict, Union, Literal, Optional

from gsuid_core.logger import logger
from aiohttp import FormData, TCPConnector, ClientSession, ContentTypeError

from .api import ARONA_URL, BATTLE_URL


class BaseBAApi:
    ssl_verify = True
    _HEADER = {}

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
        header: Dict[str, Any] = _HEADER,
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
