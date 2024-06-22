from redis import Redis, WatchError
import json
from interface.broker import BrokerInterface
from infrastructure.redis import create_connection
from libs.exceptions.connect_exception import ConnectionException
from libs.constants.error_codes import ERROR_CONNECTION


class Broker(BrokerInterface):
    _conn: Redis

    def __init__(self):
        try:
            self._conn = create_connection()
        except:
            raise ConnectionException(
                ERROR_CONNECTION, "Redis cannot create connection"
            )

    def set(self, id: str, value: str, expired: int) -> bool:
        return self._conn.setex(id, expired, value)

    def get(self, id: str) -> str:
        resp = self._conn.get(id)
        return str(resp, "UTF-8") if resp is not None else ""

    def delete(self, id: str) -> bool:
        return self._conn.delete(id) > 0

    def increase(self, id: str) -> int:
        return self._conn.incr(id, 1)

    def decrease(self, id: str) -> int:
        return self._conn.decr(id, 1)

    def publish(self, id: str, payload: str):
        self._conn.publish(id, payload)

    def subscribe(self, id: str) -> str:
        sub = self._conn.pubsub()
        sub.subscribe(id)
        for message in sub.listen():
            if message.get("type") == "message":
                resp = message.get("data")
                return str(resp, "UTF-8") if resp is not None else ""
