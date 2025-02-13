from pydantic import BaseModel
from sqlalchemy import insert

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import BookingSchema


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = BookingSchema

    async def add_booking(self, data: BaseModel, user_id: int, room_id: int):

        room = await self.session.get(RoomsOrm, room_id)

        _data = BookingSchema(
            users_id=user_id,
            price=room.price,
            room_id=room_id,
            **data.model_dump(exclude_unset=True))

        add_booking_stmt = insert(BookingsOrm).values(**_data.model_dump(exclude_unset=True)).returning(BookingsOrm)
        result = await self.session.execute(add_booking_stmt)
        model = result.scalars().one()
        return BookingSchema.model_validate(model)
