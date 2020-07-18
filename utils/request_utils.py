import aiohttp
import asyncio
import ujson

from utils.file_utils import async_write_file, async_read_file, async_file_exist


# TODO write a command to clear cache for a certain uuid
async def uuid2name(uuid: str, cache_file_name='', retry_count=5, timeout=5):
    if not cache_file_name:
        cache_file_name = 'uuid2name_cache.json'

    # if cache file exist
    if await async_file_exist(cache_file_name):
        name_cache = await async_read_file(cache_file_name)
        name_cache_json = ujson.loads(name_cache)
        if uuid in name_cache_json:
            return name_cache_json[uuid]
    else:
        name_cache_json = dict()

    async with aiohttp.ClientSession() as session:
        while retry_count:
            try:
                async with session.get(f'https://api.mojang.com/user/profiles/{uuid.replace("-", "")}/names',
                                       timeout=timeout) as response:
                    name = (await response.json())[-1]['name']
                    name_cache_json[uuid] = name
                    await async_write_file(cache_file_name, ujson.dumps(name_cache_json))
                    return name

            except asyncio.TimeoutError:
                retry_count -= 1
