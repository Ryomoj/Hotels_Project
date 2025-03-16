from fastapi import APIRouter, HTTPException

from src.api.dependencies import DatabaseDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


# Эндпоинт на получение всех существующих бронирований
@router.get("", summary="Получение всех бронирований")
async def get_all_bookings(db: DatabaseDep):
    return await db.bookings.get_all()


# Эндпоинт на получение бронирований пользователя
@router.get("/me")
async def get_my_bookings(db: DatabaseDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


# Эндпоинт бронирования
@router.post("", summary="Новая бронь")
async def new_booking(
        user_id: UserIdDep,
        booking_data: BookingAddRequestSchema,
        db: DatabaseDep
):
    try:
        room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")

    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAddSchema(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )

    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException:
        raise HTTPException(status_code=409, detail="Не осталось свободных номеров")

    await db.commit()
    return {"Status": "Ok", "booking": booking}
