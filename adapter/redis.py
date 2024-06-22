from redis import Redis
from libs.utility import get_time, sleep
from interface.broker import BrokerInterface
from infrastructure.redis import create_connection
from libs.exceptions.connect_exception import ConnectionException
from libs.exceptions.empty_string_exception import EmptyStringException
from libs.constants.error_codes import ERROR_CONNECTION, ERROR_EMPTY_STRING


class Broker(BrokerInterface):
    _conn: Redis

    def __init__(self):
        try:
            self._conn = create_connection()
        except:
            raise ConnectionException(
                ERROR_CONNECTION, "Redis cannot create connection"
            )

    def __empty_id(self, id: str):
        if not id:
            raise EmptyStringException(ERROR_EMPTY_STRING, "The id is empty")

    def set(self, id: str, value: str, expired: int) -> bool:
        self.__empty_id(id)

        if not value:
            raise EmptyStringException(ERROR_EMPTY_STRING, "The value is empty")

        return self._conn.setex(id, expired, value)

    def get(self, id: str) -> str:
        self.__empty_id(id)
        resp = self._conn.get(id)
        return str(resp, "UTF-8") if resp is not None else ""

    def delete(self, id: str) -> bool:
        self.__empty_id(id)
        return self._conn.delete(id) > 0

    def increase(self, id: str) -> int:
        self.__empty_id(id)
        return self._conn.incr(id, 1)

    def decrease(self, id: str) -> int:
        self.__empty_id(id)
        return self._conn.decr(id, 1)

    def publish(self, id: str, payload: str) -> bool:
        self.__empty_id(id)
        if not payload:
            raise EmptyStringException(ERROR_EMPTY_STRING, "The payload is empty")

        return self._conn.publish(id, payload) > -1

    def subscribe(self, id: str, ttl: int) -> str:
        self.__empty_id(id)
        sub = self._conn.pubsub()
        sub.subscribe(id)

        if ttl < 0:
            for message in sub.listen():
                if message.get("type") == "message":
                    resp = message.get("data")
                    return str(resp, "UTF-8") if resp is not None else ""

        end = get_time(ttl)
        message = None
        while get_time() < end:
            message = sub.get_message(timeout=end - get_time())
            if message is not None and message.get("type") == "message":
                break

            sleep(0.001)

        if message is not None and message.get("type") == "message":
            resp = message.get("data")
            return str(resp, "UTF-8") if resp is not None else ""
        return ""
