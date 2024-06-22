from interface.rwlock import RWLockInterface


class RWRedlock(RWLockInterface):

    def lock(lock_id: str, mode: str, ttl: int, lock_timeout: int) -> bool:
        pass

    def unlock(lock_id: str, mode: str, lock_timeout: int) -> bool:
        pass

    def locked(lock_id: str) -> bool:
        pass

    def waitforunlock(lock_id: str) -> bool:
        pass
