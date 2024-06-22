from interface.rwlock import RWLock

class RWRedlock(RWLock):
    

    def lock(lock_id : str , ttl : int , lock_timeout : int) -> bool:
        pass

    def unlock(lock_id : str , lock_timeout : int) -> bool:
        pass

    def locked(lock_id : str) -> bool:
        pass

    def waitforunlock(lock_id : str) -> bool:
        pass