import uuid
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from adapter.redis import Broker


def benchmark_get_from_database_cached():
    message = "HELLO WORLD"
    lock_id = str(uuid.uuid4())
    broker = Broker()
    broker.set(lock_id, message, 10)

    for _ in range(1000):
        msg = broker.get(lock_id)
        assert msg == message, "Not matched"


def benchmark_set_to_database_cached():
    message = "HELLO WORLD"
    broker = Broker()
    for idx in range(1000):
        do_set = broker.set(str(idx), message, 5)
        assert do_set == True, "Error set"
