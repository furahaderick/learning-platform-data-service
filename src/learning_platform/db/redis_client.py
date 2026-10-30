import redis
from learning_platform.config import redis_url


def create_redis_client():
    client = redis.Redis.from_url(redis_url(), decode_responses=True)
    client.ping()
    return client
