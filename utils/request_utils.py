import aiohttp
import asyncio
import aiofiles

import json

file_locks = {}


# TODO write a command to clear cache for a certain uuid
async def uuid2name(uuid: str, cache_file_name='', retry_count=5, timeout=5):
    if not cache_file_name:
        cache_file_name = 'uuid2name_cache.json'

    # if cache file exist
    if await async_file_exist(cache_file_name):
        name_cache = await read_file(cache_file_name)
        name_cache_json = json.loads(name_cache)
        if uuid in name_cache_json:
            return name_cache_json[uuid]
    else:
        name_cache_json = dict()

    async with aiohttp.ClientSession() as session:
        while retry_count:
            try:
                async with session.get(f'https://api.mojang.com/user/profiles/{uuid.replace("-", "")}/names',
                                       timeout=timeout) as response:
                    name = (await response.json())[0]['name']
                    name_cache_json[uuid] = name
                    await write_file(cache_file_name, json.dumps(name_cache_json))
                    return name

            except asyncio.TimeoutError:
                retry_count -= 1


async def write_file(filename: str, file_content: str):
    if filename not in file_locks:
        file_locks[filename] = False
    if not file_locks[filename]:
        file_locks[filename] = True
        async with aiofiles.open(filename, 'w') as file:
            await file.write(file_content)
        file_locks[filename] = False
    else:
        await asyncio.sleep(0.01)
        await write_file(filename, file_content)


async def read_file(filename: str):
    async with aiofiles.open(filename) as file:
        return await file.read()


async def async_file_exist(filename: str):
    try:
        async with aiofiles.open(filename) as f:
            pass
    except FileNotFoundError:
        return False
    return True
