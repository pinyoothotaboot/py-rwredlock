import uuid
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from adapter.redis import Broker
from adapter.rwredlock import RWRedlock
from configs.config import RWLOCK_TIMEOUT


def benchmark_read_lock():
    lock_id = str(uuid.uuid4())
    broker = Broker()
    message = "HELLO WORLD"
    broker.set(lock_id, message, -1)

    rwlock = RWRedlock(broker)

    for _ in range(1000):
        rwlock.waitforunlock(lock_id)
        if rwlock.lock(lock_id, rwlock.READ, 10, RWLOCK_TIMEOUT):
            resp = broker.get(lock_id)
            assert resp == message, "Not matched"
            rwlock.unlock(lock_id, rwlock.READ, RWLOCK_TIMEOUT)
