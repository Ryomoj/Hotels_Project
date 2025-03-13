from fastapi import APIRouter

from src.api.dependencies import DatabaseDep, UserIdDep
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


# Эндпоинт на получение всех существующих бронирований
@router.get("", summary="Получение всех бронирований")
async def get_all_bookings(db: DatabaseDep):
    return await db.bookings.get_all()


# Эндпоинт на получение бронирований пользователя
@router.get("/me")
async def get_my_bookings(db: DatabaseDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


# Эндпоинт бронирования
@router.post('', summary='Новая бронь')
async def new_booking(
        user_id: UserIdDep,
        booking_data: BookingAddRequestSchema,
        db: DatabaseDep
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAddSchema(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"Status": "Ok", "booking": booking}



