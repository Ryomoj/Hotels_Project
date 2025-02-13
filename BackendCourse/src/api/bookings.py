from fastapi import APIRouter

from src.api.dependencies import DatabaseDep, UserIdDep
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


# Эндпоинт бронирования
@router.post('', summary='Новая бронь')
async def new_booking(
        user_id: UserIdDep,
        booking_data: BookingAddRequestSchema,
        db: DatabaseDep
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAddSchema(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"Status": "Ok", "booking": booking}


@router.get("", summary="Получение всех бронирований")
async def get_all_bookings(db: DatabaseDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(db: DatabaseDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
