import uuid
import multiprocessing
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List
from adapter.redis import Broker
from libs.utility import sleep, get_time
from adapter.rwredlock import RWRedlock
from configs.config import RWLOCK_TIMEOUT, RWLOCK_TTL


def sumation_number(pid: str):
    RWLOCK_TTL = 1
    resp: str = ""

    lock_id: str = "sum-123456"
    identifier: str = str(uuid.uuid4())
    broker: Broker = Broker()
    rwredlock: RWRedlock = RWRedlock(broker)
    lock_key = f"summation_lock:{lock_id}"
    new_num = 0

    for idx in range(100):
        print(f"{idx + 1} - [{pid}] - Running..")
        rwredlock.waitforunlock(lock_id, RWLOCK_TTL)

        if rwredlock.lock(
            lock_id, rwredlock.READ, identifier, RWLOCK_TTL, RWLOCK_TIMEOUT
        ):
            resp = broker.get(lock_key)
        rwredlock.unlock(lock_id, rwredlock.READ, identifier, RWLOCK_TIMEOUT)

        if not resp:
            if rwredlock.lock(
                lock_id, rwredlock.WRITE, identifier, RWLOCK_TTL, RWLOCK_TIMEOUT
            ):
                broker.set(lock_key, "0.00001", RWLOCK_TIMEOUT)
            rwredlock.unlock(lock_id, rwredlock.WRITE, identifier, RWLOCK_TIMEOUT)
        else:
            if rwredlock.lock(
                lock_id, rwredlock.WRITE, identifier, RWLOCK_TTL, RWLOCK_TIMEOUT
            ):
                new_num += float(resp)
                broker.set(lock_key, f"{new_num}", RWLOCK_TIMEOUT)
            rwredlock.unlock(lock_id, rwredlock.WRITE, identifier, RWLOCK_TIMEOUT)

        sleep(0.1)


if __name__ == "__main__":
    try:
        start = get_time()
        cpu = os.cpu_count() if os.cpu_count() is not None else 2
        processings: List[multiprocessing.Process] = []
        print("Starting program...")
        broker: Broker = Broker()
        lock_id: str = "sum-123456"
        lock_key = f"summation_lock:{lock_id}"
        broker.set(lock_key, "0.00001", RWLOCK_TIMEOUT)

        for idx in range(cpu):
            processing = multiprocessing.Process(
                target=sumation_number, args=(f"Worker-{idx}",)
            )
            processing.start()
            processings.append(processing)

        for processing in processings:
            processing.join()

        print("Join multiprocessing successed in {} sec.".format(get_time() - start))

    except KeyboardInterrupt:
        print("Exit program")
        sys.exit()
