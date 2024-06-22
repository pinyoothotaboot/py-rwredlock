import time


def get_time(ttl: int = 0) -> float:
    return time.time() + ttl


def sleep(sec: float):
    time.sleep(sec)
