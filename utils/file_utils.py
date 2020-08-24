import os
import asyncio
import aiofiles

from typing import Union

from utils.aio_utils import to_async

file_locks = dict()
file_pointer = dict()


@to_async
def async_file_exist(filename: str):
    return os.path.exists(filename)


@to_async
def async_file_size(filename: str):
    return os.path.getsize(filename)


@to_async
def async_mkdir(path: str):
    os.mkdir(path)


async def async_write_file(file_path: str, file_content: Union[str, bytes], mode: str = None):
    """
    write content to file asynchronously
    :param file_path: filename
    :param file_content: file's content
    :param mode: '' for 'w', 'b' for 'wb'
    """
    path, filename = os.path.split(file_path)
    if path and not await async_file_exist(path):
        await async_mkdir(path)

    if file_path not in file_locks:
        file_locks[file_path] = False
    if not file_locks[file_path]:
        file_locks[file_path] = True
        async with aiofiles.open(file_path, 'wb' if mode == 'b' else 'w') as file:
            await file.write(file_content)
        file_locks[file_path] = False
    else:
        await asyncio.sleep(0.01)
        await async_write_file(file_path, file_content)


async def async_read_file(filename: str, seek=0, size=-1) -> str:
    async with aiofiles.open(filename) as file:
        if seek:
            await file.seek(seek)
        return await file.read(size)


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
