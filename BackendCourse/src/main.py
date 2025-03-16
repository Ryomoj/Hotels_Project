import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from src.api.dependencies import get_db
from src.init import redis_connector
from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images


async def sent_emails_bookings_today_check_in():
    async for db in get_db():
        bookings = await db.bookings.get_bookings_with_today_check_in
        print(f"{bookings=}")


async def run_send_email_regularly():
    while True:
        await sent_emails_bookings_today_check_in()
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте проекта
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    yield
    # При выключение проекта
    await redis_connector.disconnect()


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
