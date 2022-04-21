import redis
from core import settings
from core.content import TOKEN_CONNECT


def connect_redis(db_num: int) -> redis.Redis:
    """
    连接redis
    :return:
    """
    client: redis.Redis = redis.Redis(db=db_num, **settings.REDIS_CONFIG)
    return client


TOKEN_CLIENT: redis.Redis = connect_redis(TOKEN_CONNECT)
