import redis
def get_redis_client():
    # Redis 连接配置
    REDIS_HOST = 'localhost'  # Redis 服务器的主机地址
    REDIS_PORT = 6379  # Redis 服务器的端口号

    # 创建 Redis 连接
    REDIS_CLIENT = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    return REDIS_CLIENT