import socket
import aiohttp

download_session = None


def is_ipv4(address: str) -> bool:
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False


async def get_session():
    global download_session
    if download_session is None:
        download_session = aiohttp.ClientSession()
    return download_session


async def async_download_bytes(url: str, retry_count: int = 3, timeout: int = 3) -> bytes:
    session = await get_session()

    while retry_count:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    retry_count -= 1
                    continue
        except:
            retry_count -= 1

    return b''
