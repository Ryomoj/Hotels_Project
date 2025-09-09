import logging

import redis.asyncio as _redis


class RedisConnector:
    redis: _redis.Redis

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        logging.info(f"Начинаю подключение к Redis host={self.host}, post={self.port}")
        self.redis = _redis.Redis(host=self.host, port=self.port)
        logging.info(f"Успешное подключение к Redis host={self.host}, post={self.port}")

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

redis_connector = RedisConnector(host="booking_cache", port=6379)