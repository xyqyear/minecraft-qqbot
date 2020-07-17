import asyncio
import os

from utils.file_utils import write_file, read_file, async_file_exist


def test_write_file():
    test_file_name = 'test_file'
    test_file_content = 'random_content'
    asyncio.run(write_file(test_file_name, test_file_content))
    with open(test_file_name) as f:
        assert f.read() == test_file_content
    os.remove(test_file_name)


def test_read_file():
    test_file_name = 'test_file'
    test_file_content = 'random_content'
    with open(test_file_name, 'w') as f:
        f.write(test_file_content)
    assert asyncio.run(read_file(test_file_name)) == test_file_content
    os.remove(test_file_name)


def test_async_file_exist():
    test_file_name = 'test_file0'
    with open(test_file_name, 'w') as f:
        pass
    assert asyncio.run(async_file_exist(test_file_name))
    os.remove(test_file_name)
