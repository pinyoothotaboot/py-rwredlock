import uuid
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from adapter.redis import Broker
from adapter.rwredlock import RWRedlock
from configs.config import RWLOCK_TIMEOUT


def benchmark_write_lock():
    identifier: str = str(uuid.uuid4())
    lock_id = str(uuid.uuid4())
    broker = Broker()
    rwlock = RWRedlock(broker)

    for idx in range(1000):
        rwlock.waitforunlock(lock_id)
        if rwlock.lock(lock_id, rwlock.WRITE,identifier, 10, RWLOCK_TIMEOUT):
            resp = broker.increase(lock_id)
            assert resp == idx, "Not matched"
            rwlock.unlock(lock_id, rwlock.WRITE,identifier, RWLOCK_TIMEOUT)
