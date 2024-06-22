from abc import ABC, abstractmethod


class RWLockInterface(ABC):

    @abstractmethod
    def lock(self, lock_id: str, mode: str, ttl: int, lock_timeout: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def unlock(self, lock_id: str, mode: str, lock_timeout: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def locked(self, lock_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def waitforunlock(self, lock_id: str,ttl : int) -> bool:
        raise NotImplementedError
