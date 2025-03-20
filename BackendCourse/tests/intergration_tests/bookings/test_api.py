import pytest
from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-01-01", "2025-01-22", 200),
        (1, "2025-01-02", "2025-01-23", 200),
        (1, "2025-01-03", "2025-01-24", 200),
        (1, "2025-01-04", "2025-01-25", 200),
        (1, "2025-01-05", "2025-01-26", 200),
        (1, "2025-01-06", "2025-01-27", 404),
        (1, "2025-02-01", "2025-02-07", 200),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, db, auth_ac):
    # room_id = (await db.rooms.get_all())[0].id
    response = await auth_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["Status"] == "Ok"
        assert "booking" in res


@pytest.fixture(scope="module")
async def drop_booking_table():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, bookings_count",
    [
        (1, "2025-01-01", "2025-01-22", 1),
        (1, "2025-01-02", "2025-01-23", 2),
        (1, "2025-01-03", "2025-01-24", 3),
        (1, "2025-01-04", "2025-01-25", 4),
        (1, "2025-02-01", "2025-02-07", 5),
    ],
)
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    bookings_count,
    drop_booking_table,
    auth_ac,
    db,
):
    response = await auth_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == 200

    response_my_bookings = await auth_ac.get("/bookings/me")
    assert response_my_bookings.status_code == 200

    assert len(response_my_bookings.json()) == bookings_count
