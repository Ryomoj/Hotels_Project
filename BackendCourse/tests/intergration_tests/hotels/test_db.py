from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelAddSchema
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAddSchema(title="Hotel 1 Star", location="Sochi")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()
