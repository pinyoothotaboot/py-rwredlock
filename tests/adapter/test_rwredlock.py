import unittest
import uuid
from adapter.redis import Broker
from libs.utility import sleep, get_time
from adapter.rwredlock import RWRedlock
from configs.config import RWLOCK_TIMEOUT


class TestRWRedlock(unittest.TestCase):
    _lock_id: str = str(uuid.uuid4())
    _rwredlock: RWRedlock
    _ttl: int = 5

    def setUp(self):
        broker = Broker()
        self._rwredlock = RWRedlock(broker)

    def tearDown(self):
        del self._rwredlock

    def test_reader_lock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        read_lock = self._rwredlock.lock(
            self._lock_id, self._rwredlock.READ, identifier, self._ttl, RWLOCK_TIMEOUT
        )
        locked = self._rwredlock.locked(self._lock_id)
        self._rwredlock.unlock(
            self._lock_id, self._rwredlock.READ, identifier, RWLOCK_TIMEOUT
        )
        self.assertEqual(read_lock, True)
        self.assertEqual(locked, False)  # Reader lock already access every

    def test_reader_unlock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        read_lock = self._rwredlock.lock(
            self._lock_id, self._rwredlock.READ, identifier, self._ttl, RWLOCK_TIMEOUT
        )
        locked = self._rwredlock.locked(self._lock_id)
        read_unlock = self._rwredlock.unlock(
            self._lock_id, self._rwredlock.READ, identifier, RWLOCK_TIMEOUT
        )
        self.assertEqual(read_lock, True)
        self.assertEqual(locked, False)  # Reader lock already access every
        self.assertEqual(read_unlock, True)

    def test_writer_lock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        write_lock = self._rwredlock.lock(
            self._lock_id, self._rwredlock.WRITE, identifier, self._ttl, RWLOCK_TIMEOUT
        )
        locked = self._rwredlock.locked(self._lock_id)
        self._rwredlock.unlock(
            self._lock_id, self._rwredlock.WRITE, identifier, RWLOCK_TIMEOUT
        )
        self.assertEqual(write_lock, True)
        self.assertEqual(locked, True)

    def test_writer_unlock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        write_lock = self._rwredlock.lock(
            self._lock_id, self._rwredlock.WRITE, identifier, self._ttl, RWLOCK_TIMEOUT
        )
        locked_lock = self._rwredlock.locked(self._lock_id)
        write_unlock = self._rwredlock.unlock(
            self._lock_id, self._rwredlock.WRITE, identifier, RWLOCK_TIMEOUT
        )
        locked_unlock = self._rwredlock.locked(self._lock_id)
        self.assertEqual(write_lock, True)
        self.assertEqual(locked_lock, True)
        self.assertEqual(write_unlock, True)
        self.assertEqual(locked_unlock, False)

    def test_writer_lock_with_timeout_passed(self):
        identifier: str = str(uuid.uuid4())
        write_lock = self._rwredlock.lock(
            self._lock_id, self._rwredlock.WRITE, identifier, self._ttl, RWLOCK_TIMEOUT
        )
        locked_lock = self._rwredlock.locked(self._lock_id)
        sleep(self._ttl * 2)
        locked_unlock = self._rwredlock.locked(self._lock_id)
        self.assertEqual(write_lock, True)
        self.assertEqual(locked_lock, True)
        self.assertEqual(locked_unlock, False)

    def test_waitforunlock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        start = get_time()
        write_lock = self._rwredlock.lock(
            self._lock_id, self._rwredlock.WRITE, identifier, self._ttl, RWLOCK_TIMEOUT
        )
        unlock = self._rwredlock.waitforunlock(self._lock_id)
        stop = get_time()
        self.assertEqual(write_lock, True)
        self.assertEqual(unlock, False)
        self.assertEqual(int(int(stop - start) - self._ttl), self._ttl)

if __name__ == "__main__":
    unittest.main()