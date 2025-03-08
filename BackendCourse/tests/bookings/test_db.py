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
        price=100
    )
    await db.bookings.add(booking_data)

    get_booking = await db.bookings.get_one_or_none(id=1)
    print(f"ПОЛУЧИЛ ПЕРВОЕ БРОНИРОВАНИЕ = {get_booking}")

    updated_data = BookingAddSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=1, day=1),
        date_to=date(year=2025, month=12, day=22),
        price=666
    )

    await db.bookings.edit(updated_data)

    await db.bookings.delete(id=room_id)

    await db.commit()
