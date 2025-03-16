from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException

from src.api.dependencies import DatabaseDep
from src.exceptions import DateConflictException, ObjectNotFoundException, DatabaseConflictException
from src.schemas.facilities import RoomFacilityAddSchema
from src.schemas.rooms import (
    RoomAddSchema,
    RoomPatchSchema,
    RoomAddRequestSchema,
    RoomPatchRequestSchema,
)

router = APIRouter(prefix="/hotels", tags=["Номера"])


# Эндпоинт получения существующих номеров
@router.get("/{hotel_id}/rooms", summary="Получить все номера")
async def get_rooms(
    hotel_id: int,
    db: DatabaseDep,
    date_from: date = Query(examples=["2025-02-01"]),
    date_to: date = Query(examples=["2025-02-10"]),
):
    try:
        return await db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except DateConflictException:
        raise HTTPException(status_code=409, detail="Дата выезда позже даты заезда")


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить конкретный отель по ID")
async def get_room(hotel_id: int, room_id: int, db: DatabaseDep):
    try:
        return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Комната не найдена")


# Эндпоинт создания нового номера
@router.post("/{hotel_id}/rooms", summary="Создать новый номер")
async def create_room(hotel_id: int, db: DatabaseDep, room_data: RoomAddRequestSchema = Body()):
    _room_data = RoomAddSchema(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room = await db.rooms.add(_room_data)
    except DatabaseConflictException:
        raise HTTPException(status_code=404, detail="Отель не найден")

    rooms_facilities_data = [
        RoomFacilityAddSchema(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"Status": "OK", "data": room}


# Эндпоинт для полного изменения номера отеля
@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить информацию о номере")
async def put_room(hotel_id: int, room_id: int, db: DatabaseDep, room_data: RoomAddRequestSchema):
    _room_data = RoomAddSchema(hotel_id=hotel_id, **room_data.model_dump())

    try:
        await db.rooms.edit(_room_data, id=room_id)
    except DatabaseConflictException:
        raise HTTPException(status_code=404, detail="Номер не найден")

    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"Status": "OK"}


# Эндпоинт для частичного или полного изменения номера отеля
@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичная правка отеля")
async def partially_edit_room(
    hotel_id: int, room_id: int, db: DatabaseDep, room_data: RoomPatchRequestSchema
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatchSchema(hotel_id=hotel_id, **_room_data_dict)

    try:
        await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    except DatabaseConflictException:
        raise HTTPException(status_code=404, detail="Номер не найден")

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"Status": "OK"}


# Эндпоинт для удаления номера
@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление отеля")
async def delete_room(hotel_id: int, room_id: int, db: DatabaseDep):
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except DatabaseConflictException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    await db.commit()
    return {"Status": "OK"}
