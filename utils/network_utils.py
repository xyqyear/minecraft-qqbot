import socket


def is_ipv4(address: str) -> bool:
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False
