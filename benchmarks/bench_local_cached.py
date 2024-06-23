import uuid


def benchmark_get_from_local_cached():
    message = "HELLO WORLD"
    lock_id = str(uuid.uuid4())
    cached = {}
    cached[lock_id] = message

    for idx in range(1000):
        msg = cached[lock_id]
        assert msg == message, "Not matched"


def benchmark_set_to_local_cached():
    message = "HELLO WORLD"
    cached = {}
    for idx in range(1000):
        cached[idx] = message
