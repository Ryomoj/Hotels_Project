from src.api.dependencies import UserIdDep
from src.exceptions.exceptions import ObjectNotFoundException, RoomNotFoundException, NoRoomsForBookingException
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.services.base import BaseService


class BookingsService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_filtered_my_bookings(
            self,
            user_id: UserIdDep
    ):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def new_booking(
            self,
            user_id: UserIdDep,
            booking_data: BookingAddRequestSchema
    ):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAddSchema(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump()
        )

        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        except ObjectNotFoundException as exc:
            raise NoRoomsForBookingException from exc

        await self.db.commit()
        return {"Status": "Ok", "booking": booking}

