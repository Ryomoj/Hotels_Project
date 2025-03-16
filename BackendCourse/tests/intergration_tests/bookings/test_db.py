from datetime import date

from src.schemas.bookings import BookingAddSchema


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAddSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=1, day=1),
        date_to=date(year=2025, month=12, day=12),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    # Получение данных
    booking = await db.bookings.get_one_or_none(id=new_booking.id)

    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    # Изменение данных
    updated_date = date(year=2025, month=12, day=22)
    updated_booking_data = BookingAddSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=1, day=1),
        date_to=date(year=2025, month=12, day=22),
        price=666,
    )
    await db.bookings.edit(updated_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    # Удаление данных
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
