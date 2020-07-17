from utils.request_utils import uuid2name
import os
import json
import asyncio


def test_uuid2name():
    test_uuid0 = 'b8c8679b-a0f2-468c-9b38-79d4b0f068ac'
    test_name0 = 'xyqyear'
    test_uuid1 = '5aeefcf9-4387-4195-a62f-7fa2b03b7f9a'
    test_name1 = 'ScuerMaxing'
    test_cache_file = 'test_cache_json_file'
    assert asyncio.run(uuid2name(test_uuid0, test_cache_file)) == test_name0
    with open(test_cache_file) as f:
        assert f.read() == json.dumps({test_uuid0: test_name0})
    assert asyncio.run(uuid2name(test_uuid0, test_cache_file)) == test_name0

    assert asyncio.run(uuid2name(test_uuid1, test_cache_file)) == test_name1
    with open(test_cache_file) as f:
        assert f.read() == json.dumps({test_uuid0: test_name0, test_uuid1: test_name1})
    assert asyncio.run(uuid2name(test_uuid0, test_cache_file)) == test_name0
    assert asyncio.run(uuid2name(test_uuid1, test_cache_file)) == test_name1
    os.remove(test_cache_file)
