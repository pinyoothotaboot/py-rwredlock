import sys
import uuid
from configs.config import RWLOCK_TIMEOUT
from adapter.redis import Broker
from adapter.rwredlock import RWRedlock
from libs.utility import sleep

if __name__ == "__main__":
    try:
        lock_id: str = str(uuid.uuid4())
        ttl = 5
        broker = Broker()
        rwlock = RWRedlock(broker)

        if rwlock.lock(lock_id, rwlock.WRITE, ttl, RWLOCK_TIMEOUT):
            print("TO DO WRITE", rwlock.locked(lock_id))
            print("GET READ",rwlock.lock(lock_id, rwlock.READ, ttl, RWLOCK_TIMEOUT),rwlock.locked(lock_id))
            sleep(10)
        rwlock.unlock(lock_id, rwlock.WRITE, RWLOCK_TIMEOUT)
        print("LOCKED", rwlock.locked(lock_id))

        if rwlock.lock(lock_id, rwlock.READ, ttl, RWLOCK_TIMEOUT):
            print("TO DO READ", rwlock.locked(lock_id))
            print("GET WRITE ",rwlock.lock(lock_id, rwlock.WRITE, ttl, RWLOCK_TIMEOUT),rwlock.locked(lock_id))
            sleep(10)
        rwlock.unlock(lock_id, rwlock.READ, RWLOCK_TIMEOUT)
        print("LOCKED", rwlock.locked(lock_id))

        msg = rwlock.waitforunlock(lock_id)
        print(msg)

    except KeyboardInterrupt:
        print("Exit program..")
        sys.exit()
