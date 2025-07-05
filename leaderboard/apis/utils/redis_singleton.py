import redis
from django.conf import settings
from threading import Lock

# Thread-safe Singleton for Redis client
class RedisSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    # Create a new Redis client instance using the configured URL
                    cls._instance = redis.Redis.from_url(settings.LEADERBOARD_ZSET_URL)
        return cls._instance

# Usage: from apis.utils.redis_singleton import get_redis_client
# redis_client = get_redis_client()
def get_redis_client():
    """
    Returns the singleton Redis client instance.
    Use this function to get the Redis client throughout the project.
    """
    return RedisSingleton() 