from fastapi import APIRouter

from src.api.dependencies import DatabaseDep, UserIdDep
from src.schemas.bookings import BookingAddRequestSchema

router = APIRouter(prefix='/bookings', tags=['Бронирования'])


# Эндпоинт бронирования
@router.post('/new_booking', summary='Новая бронь')
async def new_booking(
        room_id: int,
        user_id: UserIdDep,
        booking_data: BookingAddRequestSchema,
        db: DatabaseDep
):
    booking = await db.bookings.add_booking(booking_data, user_id=user_id, room_id=room_id)
    await db.commit()
    return {"Status": "Ok", "booking": booking}
