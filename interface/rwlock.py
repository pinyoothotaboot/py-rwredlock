from abc import ABC, abstractmethod 

class RWLock(ABC):

    @abstractmethod
    def lock(lock_id : str , ttl : int , lock_timeout : int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def unlock(lock_id : str , lock_timeout : int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def locked(lock_id : str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def waitforunlock(lock_id : str) -> bool:
        raise NotImplementedError