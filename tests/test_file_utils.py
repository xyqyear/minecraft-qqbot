import asyncio
import pytest
import os

from utils.file_utils import async_write_file, async_read_file, async_file_exist, async_get_new_content


@pytest.mark.asyncio
async def test_write_file():
    test_file_name = 'test_file'
    test_file_content = 'random_content'
    await async_write_file(test_file_name, test_file_content)
    with open(test_file_name) as f:
        assert f.read() == test_file_content
    os.remove(test_file_name)


@pytest.mark.asyncio
async def test_read_file():
    test_file_name = 'test_file'
    test_file_content = 'random_content'
    with open(test_file_name, 'w') as f:
        f.write(test_file_content)
    assert (await async_read_file(test_file_name)) == test_file_content
    os.remove(test_file_name)


@pytest.mark.asyncio
async def test_async_file_exist():
    test_file_name = 'test_file0'
    with open(test_file_name, 'w') as f:
        pass
    assert (await async_file_exist(test_file_name))
    os.remove(test_file_name)


@pytest.mark.asyncio
async def test_async_get_new_content():
    test_filename = 'test.log'
    with open(test_filename, 'w') as f:
        f.write('1234')

    assert (await async_get_new_content(test_filename)) == ''

    with open(test_filename, 'a') as f:
        f.write('5678')

    assert (await async_get_new_content(test_filename)) == '5678'
    assert (await async_get_new_content(test_filename)) == ''

    with open(test_filename, 'w') as f:
        f.write('90')

    assert (await async_get_new_content(test_filename)) == '90'
    assert (await async_get_new_content(test_filename)) == ''

    with open(test_filename, 'a') as f:
        f.write('8765')

    assert (await async_get_new_content(test_filename)) == '8765'
    assert (await async_get_new_content(test_filename)) == ''

    os.remove(test_filename)
