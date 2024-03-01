import asyncio
import threading

from ..utils.download_resource import download_ba_resource


async def all_start():
    await download_ba_resource()


threading.Thread(target=lambda: asyncio.run(all_start()), daemon=True).start()
