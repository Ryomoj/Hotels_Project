from sqlalchemy import select, func

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomSchema

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from,
            date_to
    ):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
