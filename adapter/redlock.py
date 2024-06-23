import logging
import logging.config
from configs.logging_setting import LOGGING

logging.config.dictConfig(LOGGING)

from libs.utility import get_time, sleep
from interface.rwlock import LockInterface
from interface.broker import BrokerInterface
from configs.config import LOCK_TIMEOUT, LOCK_TTL, LOCK_NAME

logger = logging.getLogger(__name__)


class Redlock(LockInterface):
    _broker: BrokerInterface

    def __init__(self, broker: BrokerInterface) -> None:
        self._broker = broker

    def __get__lock_id(self, lock_id: str) -> str:
        return f"{LOCK_NAME}:{lock_id}"

    def lock(
        self,
        lock_id: str,
        indentifier: str,
        ttl: int = LOCK_TTL,
        lock_timeout: int = LOCK_TIMEOUT,
    ) -> bool:
        lock_timeout: int = lock_timeout if lock_timeout > 0 else LOCK_TIMEOUT
        ttl: int = ttl if ttl > 0 else LOCK_TTL
        end = get_time(ttl)
        lock_id = self.__get__lock_id(lock_id)

        while get_time() < end:
            resp: str = self._broker.get(lock_id)
            if not resp:
                # If somebody not use lock
                # Then can set lock
                while self._broker.set(lock_id, indentifier, lock_timeout):
                    return True
            else:
                # You stay used lock
                if resp == indentifier:
                    return True

            sleep(0.01)

        return False

    def unlock(
        self, lock_id: str, indentifier: str, ttl: int, lock_timeout: int
    ) -> bool:
        lock_timeout: int = lock_timeout if lock_timeout > 0 else LOCK_TIMEOUT
        ttl: int = ttl if ttl > 0 else LOCK_TTL
        end = get_time(ttl)
        lock_id = self.__get__lock_id(lock_id)

        while get_time() < end:
            resp: str = self._broker.get(lock_id)
            # Not found someone use lock
            if not resp:
                return True

            # Other using lock
            if resp != indentifier:
                return False

            # Remove lock
            while self._broker.delete(lock_id):
                return True

            sleep(0.01)

        return False

    def locked(self, lock_id: str) -> bool:
        lock_id = self.__get__lock_id(lock_id)
        while self._broker.get(lock_id):
            return True
        return False

    def waitforunlock(self, lock_id: str, ttl: int) -> bool:
        flag: bool = True
        if ttl < 0:
            while flag:
                flag = self.locked(lock_id)
                sleep(0.1)
            return flag

        end = get_time(ttl)
        while (get_time() < end):
            flag = self.locked(lock_id)
            if not flag:
                return flag
            
            sleep(0.1)

        return flag
