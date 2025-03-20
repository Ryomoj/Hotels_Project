# ruff: noqa: E402, F403
import json
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool  # noqa
from src.main import app
from src.models import *
from httpx import AsyncClient, ASGITransport

from src.schemas.hotels import HotelAddSchema
from src.schemas.rooms import RoomAddSchema
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db():
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as mock_hotels_file:
        hotels_data = json.load(mock_hotels_file)
    with open("tests/mock_rooms.json", encoding="utf-8") as mock_hotels_file:
        rooms_data = json.load(mock_hotels_file)

    hotels_list = [HotelAddSchema.model_validate(hotel) for hotel in hotels_data]
    rooms_list = [RoomAddSchema.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_list)
        await db_.rooms.add_bulk(rooms_list)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def test_register_user(ac, setup_database):
    await ac.post("/auth/register", json={"email": "kot@pes.com", "password": "1234"})
    print("ПОЛЬЗОВАТЕЛЬ ЗАРЕГИСТРИРОВАЛСЯ")


@pytest.fixture(scope="session")
async def auth_ac(ac, test_register_user):
    await ac.post("/auth/login", json={"email": "kot@pes.com", "password": "1234"})
    assert ac.cookies["access_token"]
    yield ac


# Так пишутся обычные декораторы

# def empty_cache(*args, **kwargs):
#     def wrapper(func):
#         def inner():
#             res = func(*args, **kwargs)
#             return res
#         return inner
#     return wrapper


# def empty_cache(*args, **kwargs):
#     def wrapper(func):
#         return func
#     return wrapper
