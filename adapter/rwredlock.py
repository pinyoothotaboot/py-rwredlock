import uuid
import json
from libs.utility import get_time,sleep
from interface.rwlock import RWLockInterface
from interface.broker import BrokerInterface
from configs.config import RWLOCK_READER,RWLOCK_WRITER,RWLOCK_TIMEOUT,RWLOCK_TTL

"""
    Implement ref : https://en.wikipedia.org/wiki/Readers%E2%80%93writer_lock
"""
class RWRedlock(RWLockInterface):
    _broker : BrokerInterface
    READ : str = RWLOCK_READER
    WRITE : str = RWLOCK_WRITER

    def __init__(self,broker : BrokerInterface) -> None:
        self._broker = broker
    
    def __get_write_lock_id(self,lock_id : str) -> str:
        return f"lock:{self.WRITE}:{lock_id}"
    
    def __get_read_lock_id(self,lock_id : str) -> str:
        return f"lock:{self.READ}:{lock_id}"
    
    def __lock_read(self,lock_id: str, ttl: int, lock_timeout: int) -> bool:
        lock_timeout : int = lock_timeout if lock_timeout > 0 else RWLOCK_TIMEOUT
        ttl : int = ttl if ttl > 0 else RWLOCK_TTL
        end = get_time(ttl)

        reader : str = self.__get_read_lock_id(lock_id)
        writer : str = self.__get_write_lock_id(lock_id)

        writer_icr : str = f"inc:{writer}"
        reader_icr : str = f"inc:{reader}"

        # Lock g
        while self._broker.set(lock_id,reader,lock_timeout):
            break

        writer_active : str = self._broker.get(writer)
        num_writers_waiting : str = self._broker.get(writer_icr)

        # While num_writers_waiting > 0 or writer_active
        while writer_active or (num_writers_waiting and int(num_writers_waiting) > 0):
            if get_time() > end:
                # Unlock g.
                while self._broker.delete(lock_id):
                    break
                return False

            writer_active : str = self._broker.get(writer)
            num_writers_waiting : str = self._broker.get(writer_icr)

            sleep(0.001)
        
        # Increment num_readers_active
        num_readers_active : str = self._broker.get(reader_icr)
        if not num_readers_active:
            num_readers_active : str = "1"
            while self._broker.set(reader_icr,num_readers_active,lock_timeout):
                break
        else:
            num_readers_active : str = self._broker.increase(reader_icr)

        # Unlock g
        while self._broker.delete(lock_id):
            break

        return int(num_readers_active) > 0
                                
    def __unlock_read(self,lock_id: str, lock_timeout: int) -> bool:
        lock_timeout : int = lock_timeout if lock_timeout > 0 else RWLOCK_TIMEOUT
        reader : str = self.__get_read_lock_id(lock_id)

        reader_icr : str = f"inc:{reader}"

        # Lock g
        while self._broker.set(lock_id,reader,lock_timeout):
            break

        # Decrement num_readers_active
        num_readers_active : str = self._broker.decrease(reader_icr)

        # If num_readers_active = 0
        if num_readers_active and int(num_readers_active) < 1:
            while self._broker.delete(reader):
                break

            while self._broker.delete(reader_icr):
                break

        # Unlock g.
        while self._broker.delete(lock_id):
            return True
        
        return False

    def __lock_write(self,lock_id: str, ttl: int, lock_timeout: int) -> bool:
        lock_timeout : int = lock_timeout if lock_timeout > 0 else RWLOCK_TIMEOUT
        ttl : int = ttl if ttl > 0 else RWLOCK_TTL
        end = get_time(ttl)

        reader : str = self.__get_read_lock_id(lock_id)
        writer : str = self.__get_write_lock_id(lock_id)

        writer_icr : str = f"inc:{writer}"

        flag_writer : bool = False

        # Lock g
        while self._broker.set(lock_id,writer,lock_timeout):
            break

        # Increment num_writers_waiting
        num_writers_waiting : str = self._broker.get(writer_icr)
        if not writer_icr:
            num_writers_waiting = "1"
            while self._broker.set(writer_icr,num_writers_waiting,lock_timeout):
                break
        else:
            num_writers_waiting : str = self._broker.increase(writer_icr)


        num_readers_active : str = self._broker.get(reader)
        writer_active  : str = self._broker.get(writer)
        while (num_readers_active and int(num_readers_active) > 0) or writer_active:
            if get_time() > end:
                # Unlock g.
                while self._broker.delete(lock_id):
                    break
                return False
            sleep(0.001)
        
        # Decrement num_writers_waiting
        num_writers_waiting = self._broker.decrease(writer_icr)
        while num_writers_waiting and int(num_writers_waiting) > 0:
            num_writers_waiting = self._broker.decrease(writer_icr)

        # Set writer_active to true
        while self._broker.set(writer,"1",lock_timeout):
            flag_writer = True
            break

        # Unlock g
        while self._broker.delete(lock_id):
            break
        
        return flag_writer

    def __unlock_write(self,lock_id: str, lock_timeout: int) -> bool:
        writer : str = self.__get_write_lock_id(lock_id)
        reader : str = self.__get_read_lock_id(lock_id)

        writer_icr : str = f"inc:{writer}"
        reader_icr : str = f"inc:{reader}"

        # Lock g
        while self._broker.set(lock_id,writer,lock_timeout):
            break

        # Set writer_active to false
        while self._broker.delete(writer):
            break

        while self._broker.delete(reader):
            break

        while self._broker.delete(writer_icr):
            break

        while self._broker.delete(reader_icr):
            break

        # Unlock g
        while self._broker.delete(lock_id):
            return True
        
        return False

    def lock(self,lock_id: str, mode: str, ttl: int, lock_timeout: int) -> bool:
        print(f"[{mode}] - Get lock id : {lock_id}")
        if mode == self.READ:
            return self.__lock_read(lock_id,ttl,lock_timeout)
        return self.__lock_write(lock_id,ttl,lock_timeout)

    def unlock(self,lock_id: str, mode: str, lock_timeout: int) -> bool:
        print(f"[{mode}] - Release lock id : {lock_id}")
        if mode == self.READ:
            return self.__unlock_read(lock_id,lock_timeout)
        return self.__unlock_write(lock_id,lock_timeout)

    def locked(self,lock_id: str) -> bool:
        writer : str = self.__get_write_lock_id(lock_id)
        resp_write : str = self._broker.get(writer)
        return True if resp_write else False

    def waitforunlock(self,lock_id: str,ttl : int = -1) -> bool:
        flag : bool = True
        if ttl < 0:
            while flag:
                flag = self.locked(lock_id)
                sleep(0.1)
            return flag
        
        end = get_time(ttl)
        while (get_time() < end) or flag:
            flag = self.locked(lock_id)
            sleep(0.1)
        
        return flag

            
        
