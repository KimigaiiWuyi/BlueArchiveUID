from gsuid_core.server import on_core_start

from ..utils.download_resource import download_ba_resource


@on_core_start
async def all_start():
    await download_ba_resource()
