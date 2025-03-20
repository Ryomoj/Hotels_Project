from fastapi import APIRouter

from src.api.dependencies import DatabaseDep, UserIdDep
from src.exceptions.exceptions import NoRoomsForBookingException, NoRoomsForBookingFoundHTTPException
from src.schemas.bookings import BookingAddRequestSchema
from src.services.bookings import BookingsService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


# Эндпоинт на получение всех существующих бронирований
@router.get("", summary="Получение всех бронирований")
async def get_all_bookings(db: DatabaseDep):
    return await BookingsService(db).get_all_bookings()


# Эндпоинт на получение бронирований пользователя
@router.get("/me")
async def get_my_bookings(db: DatabaseDep, user_id: UserIdDep):
    return await BookingsService(db).get_filtered_my_bookings(user_id=user_id)


# Эндпоинт бронирования
@router.post("", summary="Новая бронь")
async def new_booking(
        user_id: UserIdDep,
        booking_data: BookingAddRequestSchema,
        db: DatabaseDep
):
    try:
        booking = await BookingsService(db).new_booking(user_id, booking_data)
    except NoRoomsForBookingException:
        raise NoRoomsForBookingFoundHTTPException
    return {"Status": "Ok", "booking": booking}
