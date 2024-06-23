import logging
import logging.config
from configs.logging_setting import LOGGING

logging.config.dictConfig(LOGGING)

from libs.utility import get_time, sleep
from interface.rwlock import LockInterface
from interface.broker import BrokerInterface
from configs.config import (
    RWLOCK_READER,
    RWLOCK_WRITER,
    RWLOCK_TIMEOUT,
    RWLOCK_TTL,
    RWLOCK_NAME,
)

logger = logging.getLogger(__name__)

"""
    Implement ref : https://en.wikipedia.org/wiki/Readers%E2%80%93writer_lock
"""


class RWRedlock(LockInterface):
    _broker: BrokerInterface
    READ: str = RWLOCK_READER
    WRITE: str = RWLOCK_WRITER

    def __init__(self, broker: BrokerInterface) -> None:
        self._broker = broker

    def __get_write_lock_id(self, lock_id: str) -> str:
        return f"{RWLOCK_NAME}:{self.WRITE}:{lock_id}"

    def __get_read_lock_id(self, lock_id: str) -> str:
        return f"{RWLOCK_NAME}:{self.READ}:{lock_id}"

    def __lock_read(self, lock_id: str, ttl: int, lock_timeout: int) -> bool:
        lock_timeout: int = lock_timeout if lock_timeout > 0 else RWLOCK_TIMEOUT
        ttl: int = ttl if ttl > 0 else RWLOCK_TTL
        end = get_time(ttl)

        reader: str = self.__get_read_lock_id(lock_id)
        writer: str = self.__get_write_lock_id(lock_id)

        writer_icr: str = f"inc:{writer}"
        reader_icr: str = f"inc:{reader}"

        # Lock g
        while self._broker.set(lock_id, reader, lock_timeout):
            break

        writer_active: str = self._broker.get(writer)
        num_writers_waiting: str = self._broker.get(writer_icr)

        # While num_writers_waiting > 0 or writer_active
        while writer_active or (num_writers_waiting and int(num_writers_waiting) > 0):
            if get_time() > end:
                # Unlock g.
                while self._broker.delete(lock_id):
                    break
                return False

            writer_active: str = self._broker.get(writer)
            num_writers_waiting: str = self._broker.get(writer_icr)

            sleep(0.01)

        # Increment num_readers_active
        num_readers_active: str = self._broker.get(reader_icr)
        if not num_readers_active:
            num_readers_active: str = "1"
            while self._broker.set(reader_icr, num_readers_active, lock_timeout):
                break
        else:
            num_readers_active: str = self._broker.increase(reader_icr)

        # Unlock g
        while self._broker.delete(lock_id):
            break

        return int(num_readers_active) > 0

    def __unlock_read(self, lock_id: str, lock_timeout: int) -> bool:
        lock_timeout: int = lock_timeout if lock_timeout > 0 else RWLOCK_TIMEOUT
        reader: str = self.__get_read_lock_id(lock_id)

        reader_icr: str = f"inc:{reader}"

        # Lock g
        while self._broker.set(lock_id, reader, lock_timeout):
            break

        # Decrement num_readers_active
        num_readers_active: str = self._broker.decrease(reader_icr)

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

    def __lock_write(self, lock_id: str, ttl: int, lock_timeout: int) -> bool:
        lock_timeout: int = lock_timeout if lock_timeout > 0 else RWLOCK_TIMEOUT
        ttl: int = ttl if ttl > 0 else RWLOCK_TTL
        end = get_time(ttl)

        reader: str = self.__get_read_lock_id(lock_id)
        writer: str = self.__get_write_lock_id(lock_id)

        writer_icr: str = f"inc:{writer}"

        flag_writer: bool = False

        # Lock g
        while self._broker.set(lock_id, writer, lock_timeout):
            break

        # Increment num_writers_waiting
        num_writers_waiting: str = self._broker.get(writer_icr)
        if not writer_icr:
            num_writers_waiting = "1"
            while self._broker.set(writer_icr, num_writers_waiting, lock_timeout):
                break
        else:
            num_writers_waiting: str = self._broker.increase(writer_icr)

        num_readers_active: str = self._broker.get(reader)
        writer_active: str = self._broker.get(writer)
        while (num_readers_active and int(num_readers_active) > 0) or writer_active:
            if get_time() > end:
                while self._broker.delete(writer_icr):
                    break

                # Unlock g.
                while self._broker.delete(lock_id):
                    break
                return False
            sleep(0.01)

        # Decrement num_writers_waiting
        self._broker.delete(writer_icr)

        # Set writer_active to true
        while self._broker.set(writer, "1", lock_timeout):
            flag_writer = True
            break

        # Unlock g
        while self._broker.delete(lock_id):
            break

        return flag_writer

    def __unlock_write(self, lock_id: str, lock_timeout: int) -> bool:
        writer: str = self.__get_write_lock_id(lock_id)
        reader: str = self.__get_read_lock_id(lock_id)

        writer_icr: str = f"inc:{writer}"
        reader_icr: str = f"inc:{reader}"

        # Lock g
        while self._broker.set(lock_id, writer, lock_timeout):
            break

        # Clear all reader and write id
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

    """
        Function : lock
        @sync
        About : Request acquire distribute RWLocking
        Param :
            - lock_id (string) : The identifie key to acquire distribute locking
            - mode (string) : Mode request acquire READ / WRITE
            - ttl (integer) : Time to live request acquire distribute locking
            - lock_timeout (integer) : The timeout of set in lock
        Return :
            - acquire (boolean) : Status request acquire distribute locking
    """

    def lock(self, lock_id: str, mode: str, ttl: int, lock_timeout: int) -> bool:
        if mode == self.READ:
            acquire = self.__lock_read(lock_id, ttl, lock_timeout)
            if acquire:
                logger.info(f"[{mode}] - Acquired lock id : {lock_id}")
            return acquire
        acquire = self.__lock_write(lock_id, ttl, lock_timeout)
        if acquire:
            logger.info(f"[{mode}] - Acquired lock id : {lock_id}")
        return acquire

    """
        Function : unlock
        @sync
        About : Request release acquired distribute locking
        Param :
            - lock_id (string) : The identifie key to acquire distribute locking
            - mode (string) : Mode request acquire READ / WRITE
            - lock_timeout (integer) : The timeout of set in lock
        Return :
            - release (boolean) : Status request release acquired distribute locking
    """

    def unlock(self, lock_id: str, mode: str, lock_timeout: int) -> bool:
        if mode == self.READ:
            release = self.__unlock_read(lock_id, lock_timeout)
            if release:
                logger.info(f"[{mode}] - Release lock id : {lock_id}")
            return release
        release = self.__unlock_write(lock_id, lock_timeout)
        if release:
            logger.info(f"[{mode}] - Release lock id : {lock_id}")
        return release

    """
        Function : locked
        @sync
        About : Check status read or write locking 
        Param :
            - lock_id (string) : The identifie key to acquire distribute locking
        Return :
            - (boolean) : The status READ / WRITE locking
    """

    def locked(self, lock_id: str) -> bool:
        writer: str = self.__get_write_lock_id(lock_id)
        resp_write: str = self._broker.get(writer)
        return True if resp_write else False

    """
        Function : waitforunlock
        @sync
        About : Waiting for current locking release
        Param :
            - lock_id (string) : The identifie key to acquire distribute locking
            - ttl (integer) : Time to live request acquire distribute locking
        Return :
            - flag (boolean) : The flag status of READ / WRITE locking 
    """

    def waitforunlock(self, lock_id: str, ttl: int = -1) -> bool:
        flag: bool = True
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
