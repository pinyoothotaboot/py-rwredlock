# RWRedlock
## _The distribute locking implement by RWLock_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This project created for implement redis with RWLocking.The project create concept by [Readers–writer_lock](https://en.wikipedia.org/wiki/Readers%E2%80%93writer_lock).Support python 100%

## Features

- RWRedlock : The readers and writer locking implement in distribute architecture (default use redis)

## Installation

This project requires [Python](https://www.python.org/downloads/)

## Redis
```sh
sudo apt install redis-server
```

## Development

You can improve the source code to implement to project 

Install dependencies:

```sh
virtaulenv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Run normal:

```sh
python app.py
```

Run unittest

```sh
python -m unittest
```

## Test reports
```sh
INFO [reader] - Acquired lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
INFO [reader] - Release lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
INFO [reader] - Acquired lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
INFO [reader] - Release lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
INFO [writer] - Acquired lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
INFO [writer] - Acquired lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
INFO [writer] - Release lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
INFO [writer] - Acquired lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
INFO [writer] - Acquired lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
INFO [writer] - Release lock id : 520f2a38-8fac-47fa-9b6a-76739c2eadc3
.
----------------------------------------------------------------------
Ran 21 tests in 20.161s

OK
```

## Example

```py
import uuid
from configs.config import RWLOCK_TIMEOUT
from adapter.redis import Broker
from adapter.rwredlock import RWRedlock

lock_id: str = str(uuid.uuid4())
ttl = 5
broker = Broker()
rwlock = RWRedlock(broker)

if rwlock.lock(lock_id, rwlock.WRITE, ttl, RWLOCK_TIMEOUT):
    # Do Something
    
rwlock.unlock(lock_id, rwlock.WRITE, RWLOCK_TIMEOUT)
```

## Incomming

- Benchmarks
- Distribute mutex lock (Redlock) , One write , one read key
- Support other broker , MongoDb , Postgres etc.
- Optimizations

## License

[MIT](https://github.com/pinyoothotaboot/py-rwlock/blob/main/LICENSE)

## Author
_Pinyoo Thotaboot_
