from django.core.cache.backends.base import BaseCache, DEFAULT_TIMEOUT

from google.appengine.api import memcache


class GAECache(BaseCache):
    "An implementation of a cache binding using AppEngine's memcache API"

    def __init__(self, location, params):
        super(self.__class__, self).__init__(params)

    @property
    def _client(self):
        if getattr(self, '_gae_client', None) is None:
            self._gae_client = memcache.Client()
        return self._gae_client

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        if timeout is DEFAULT_TIMEOUT:
            return self._client.add(key, value)
        return self._client.add(key, value, time=timeout)

    def get(self, key, default=None, version=None):
        value = self._client.get(key)
        return default if value is None else value

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        if timeout is DEFAULT_TIMEOUT:
            return self._client.set(key, value)
        return self._client.set(key, value, time=timeout)

    def delete(self, key, version=None):
        return self._client.delete(key) == memcache.DELETE_SUCCESSFUL

    def get_many(self, keys, version=None):
        return self._client.get_multi(keys)

    def incr(self, key, delta=1, version=None, initial_value=None):
        new_value = self._client.incr(key, delta=delta, initial_value=initial_value)
        if new_value is None:
            raise ValueError("Key \"{}\" is not in cache.".format(key))
        return new_value

    def decr(self, key, delta=1, version=None, initial_value=None):
        new_value = self._client.incr(key, delta=delta, initial_value=initial_value)
        if new_value is None:
            raise ValueError("Key \"{}\" is not in cache.".format(key))
        return new_value

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        if timeout is DEFAULT_TIMEOUT:
            return self._client.set_multi(data)
        return self._client.set_multi(data, time=DEFAULT_TIMEOUT)

    def delete_many(self, keys, version=None):
        return self._client.delete_multi(keys)

    def clear(self):
        return self._client.flush_all()

    def incr_version(self, key, delta=1, version=None):
        pass

    def decr_version(self, key, delta=1, version=None):
        pass

    def close(self, **kwargs):
        pass