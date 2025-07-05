from abc import ABC, abstractmethod

class CacheAdapter(ABC):
    """
    Abstract base class for cache adapters.
    Implementations should provide zadd, zscore, zrevrange, zrevrank, and delete methods.
    """
    @abstractmethod
    def zadd(self, key, mapping):
        pass

    @abstractmethod
    def zscore(self, key, member):
        pass

    @abstractmethod
    def zrevrange(self, key, start, end, withscores=False):
        pass

    @abstractmethod
    def zrevrank(self, key, member):
        pass

    @abstractmethod
    def delete(self, key):
        pass

class RedisCacheAdapter(CacheAdapter):
    """
    Adapter for Redis cache backend.
    Wraps a redis.Redis client to provide a unified interface.
    """
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def zadd(self, key, mapping):
        return self.redis_client.zadd(key, mapping)

    def zscore(self, key, member):
        return self.redis_client.zscore(key, member)

    def zrevrange(self, key, start, end, withscores=False):
        return self.redis_client.zrevrange(key, start, end, withscores=withscores)

    def zrevrank(self, key, member):
        return self.redis_client.zrevrank(key, member)

    def delete(self, key):
        return self.redis_client.delete(key) 