import asyncio
import aiofiles

file_locks = {}


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
