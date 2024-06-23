import os
from dotenv import load_dotenv

load_dotenv()

# Load redis config from env
REDIS_HOST: str = os.getenv("REDIS_HOST") if os.getenv("REDIS_HOST") else "127.0.0.1"
REDIS_PORT: int = int(os.getenv("REDIS_PORT")) if os.getenv("REDIS_PORT") else 6739
REDIS_DATABASE: int = (
    int(os.getenv("REDIS_DATABASE")) if os.getenv("REDIS_DATABASE") else 0
)
REDIS_USER: str = os.getenv("REDIS_USER")
REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")

# Load RWLocking config from env
RWLOCK_NAME: str = os.getenv("RWLOCK_NAME") if os.getenv("RWLOCK_NAME") else "rwlock"
RWLOCK_READER: str = (
    os.getenv("RWLOCK_READER") if os.getenv("RWLOCK_READER") else "reader"
)
RWLOCK_WRITER: str = (
    os.getenv("RWLOCK_WRITER") if os.getenv("RWLOCK_WRITER") else "writer"
)
RWLOCK_TIMEOUT: int = (
    int(os.getenv("RWLOCK_TIMEOUT")) if os.getenv("RWLOCK_TIMEOUT") else 10
)  # Sec
RWLOCK_TTL: int = int(os.getenv("RWLOCK_TTL")) if os.getenv("RWLOCK_TTL") else 10  # Sec

# Load Locking config from env
LOCK_NAME : str = os.getenv("LOCK_NAME") if os.getenv("LOCK_NAME") else "lock"
LOCK_TIMEOUT : int = int(os.getenv("LOCK_TIMEOUT")) if os.getenv("LOCK_TIMEOUT") else 10
LOCK_TTL : int = int(os.getenv("LOCK_TTL")) if os.getenv("LOCK_TTL") else 10
