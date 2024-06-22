import redis
from configs.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USER,
    REDIS_PASSWORD,
    REDIS_DATABASE,
)


def create_connection(is_cluster: bool = False) -> redis.Redis:
    if is_cluster:
        # TODO :: Incoming
        return redis.RedisCluster(host=REDIS_HOST, port=REDIS_PORT)

    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        username=REDIS_USER,
        password=REDIS_PASSWORD,
        db=REDIS_DATABASE,
    )
