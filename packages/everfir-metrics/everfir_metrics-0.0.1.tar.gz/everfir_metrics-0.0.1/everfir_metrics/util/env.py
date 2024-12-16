import os

def get_container_ip() -> str:
    return os.getenv("PodIP", "unknown")


def get_env() -> str:
    return os.getenv("ENV", "unknown")


def test() -> None:
    pass

__all__ = ["get_container_ip", "get_env"]