import asyncio
import aiofiles

from aiofiles import os as async_os

file_locks = dict()
file_pointer = dict()


async def async_write_file(filename: str, file_content: str):
    if filename not in file_locks:
        file_locks[filename] = False
    if not file_locks[filename]:
        file_locks[filename] = True
        async with aiofiles.open(filename, 'w') as file:
            await file.write(file_content)
        file_locks[filename] = False
    else:
        await asyncio.sleep(0.01)
        await async_write_file(filename, file_content)


async def async_read_file(filename: str, seek=0, size=-1) -> str:
    async with aiofiles.open(filename) as file:
        if seek:
            await file.seek(seek)
        return await file.read(size)


async def async_file_exist(filename: str) -> bool:
    try:
        async with aiofiles.open(filename) as f:
            pass
    except FileNotFoundError:
        return False
    return True


async def async_file_size(filename: str) -> int:
    return (await async_os.stat(filename)).st_size


async def async_get_new_content(filename: str) -> str:
    file_size = await async_file_size(filename)
    if filename not in file_pointer:
        file_pointer[filename] = file_size
        return ''

    last_pointer_position = file_pointer[filename]
    if last_pointer_position == file_size:
        return ''
    file_pointer[filename] = file_size

    if file_size < last_pointer_position:
        return await async_read_file(filename)
    else:
        return await async_read_file(filename, last_pointer_position, file_size - last_pointer_position)
