from glaucus.settings import REDIS_DB
from glaucus.settings import REDIS_HOST
from glaucus.settings import REDIS_PORT
import redis
import logging

from tools.base import InternalError

logger = logging.getLogger(__file__)

class RedisService():

    @staticmethod
    def __get_connect():
        try:
            conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        except Exception:
            logger.error(f"Can't connect to redis {REDIS_HOST}, {REDIS_PORT}, {REDIS_DB}")
            raise InternalError
        return conn

    @staticmethod
    def get_key(key, default_value=None):
        conn = RedisService.__get_connect()
        value = conn.get(key)
        if not value:
            return default_value
        return value

    @staticmethod
    def set_key(key, value, expire_time=None):
        conn = RedisService.__get_connect()
        if not expire_time:
            conn.set(key, value)
        else:
            conn.setex(key, expire_time, value)
        return True
