from utils.request_utils import uuid2name, write_file, read_file, async_file_exist
import os
import json
import asyncio


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


def test_uuid2name():
    test_uuid0 = 'b8c8679b-a0f2-468c-9b38-79d4b0f068ac'
    test_name0 = 'xyqyear'
    test_cache_file = 'test_cache_json_file'
    assert asyncio.run(uuid2name(test_uuid0, test_cache_file)) == test_name0
    with open(test_cache_file) as f:
        assert f.read() == json.dumps({test_uuid0: test_name0})
    assert asyncio.run(uuid2name(test_uuid0, test_cache_file)) == test_name0
    os.remove(test_cache_file)
