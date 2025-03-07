import json

import pytest

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from httpx import AsyncClient, ASGITransport

from src.schemas.hotels import HotelAddSchema
from src.schemas.rooms import RoomAddSchema
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def insert_mock_data(setup_database):
    with open("tests/mock_hotels.json", "r") as file:
        data = json.loads(file.read())

        async with DBManager(session_factory=async_session_maker_null_pool) as db:
            for i in range(len(data)):
                hotel_data = HotelAddSchema(title=data[i]["title"], location=data[i]["location"])
                await db.hotels.add(hotel_data)

            await db.commit()

    with open("tests/mock_rooms.json", "r") as file:
        data = json.loads(file.read())

        async with DBManager(session_factory=async_session_maker_null_pool) as db:
            for i in range(len(data)):
                room_data = RoomAddSchema(
                    hotel_id=data[i]["hotel_id"],
                    title=data[i]["title"],
                    description=data[i]["description"],
                    price=data[i]["price"],
                    quantity=data[i]["quantity"]
                )
                print(room_data)
                await db.rooms.add(room_data)

            await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def test_register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )
