import unittest
import uuid
from adapter.redis import Broker
from libs.utility import sleep, get_time
from adapter.redlock import Redlock
from configs.config import LOCK_TIMEOUT


class TestRedlock(unittest.TestCase):
    _lock_id: str = str(uuid.uuid4())
    _edlock: Redlock
    _ttl: int = 5

    def setUp(self):
        broker = Broker()
        self._redlock = Redlock(broker)

    def tearDown(self):
        del self._redlock

    def test_reader_lock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        read_lock = self._redlock.lock(
            self._lock_id, identifier, self._ttl, LOCK_TIMEOUT
        )
        locked = self._redlock.locked(self._lock_id)
        self._redlock.unlock(self._lock_id, identifier, self._ttl, LOCK_TIMEOUT)
        self.assertEqual(read_lock, True)
        self.assertEqual(locked, True)

    def test_reader_unlock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        read_lock = self._redlock.lock(
            self._lock_id, identifier, self._ttl, LOCK_TIMEOUT
        )
        locked = self._redlock.locked(self._lock_id)
        read_unlock = self._redlock.unlock(
            self._lock_id, identifier, self._ttl, LOCK_TIMEOUT
        )
        self.assertEqual(read_lock, True)
        self.assertEqual(locked, True)
        self.assertEqual(read_unlock, True)

    def test_writer_lock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        write_lock = self._redlock.lock(
            self._lock_id, identifier, self._ttl, LOCK_TIMEOUT
        )
        locked = self._redlock.locked(self._lock_id)
        self._redlock.unlock(self._lock_id, identifier, self._ttl, LOCK_TIMEOUT)
        self.assertEqual(write_lock, True)
        self.assertEqual(locked, True)

    def test_writer_unlock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        write_lock = self._redlock.lock(
            self._lock_id, identifier, self._ttl, LOCK_TIMEOUT
        )
        locked_lock = self._redlock.locked(self._lock_id)
        write_unlock = self._redlock.unlock(
            self._lock_id, identifier, self._ttl, LOCK_TIMEOUT
        )
        locked_unlock = self._redlock.locked(self._lock_id)
        self.assertEqual(write_lock, True)
        self.assertEqual(locked_lock, True)
        self.assertEqual(write_unlock, True)
        self.assertEqual(locked_unlock, False)

    def test_writer_lock_with_timeout_passed(self):
        identifier: str = str(uuid.uuid4())
        write_lock = self._redlock.lock(
            self._lock_id, identifier, self._ttl, LOCK_TIMEOUT
        )
        locked_lock = self._redlock.locked(self._lock_id)
        sleep(self._ttl * 2)
        locked_unlock = self._redlock.locked(self._lock_id)
        self.assertEqual(write_lock, True)
        self.assertEqual(locked_lock, True)
        self.assertEqual(locked_unlock, False)

    def test_waitforunlock_with_data_passed(self):
        identifier: str = str(uuid.uuid4())
        start = get_time()
        write_lock = self._redlock.lock(
            self._lock_id, identifier, self._ttl, LOCK_TIMEOUT
        )
        unlock = self._redlock.waitforunlock(self._lock_id, self._ttl)
        stop = get_time()
        self.assertEqual(write_lock, True)
        self.assertEqual(unlock, False)
        self.assertEqual(int(int(stop - start) - self._ttl), self._ttl)
