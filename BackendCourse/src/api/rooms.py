import logging
from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DatabaseDep
from src.exceptions.exceptions import (ObjectNotFoundException,
                                       RoomNotFoundHTTPException,
                                       HotelNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
                                       )
from src.schemas.rooms import (
    RoomAddRequestSchema,
    RoomPatchRequestSchema,
)
from src.services.hotels import HotelsService
from src.services.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["Номера"])


# Эндпоинт получения существующих номеров
@router.get("/{hotel_id}/rooms", summary="Получить все номера")
async def get_rooms(
        hotel_id: int,
        db: DatabaseDep,
        date_from: date = Query(examples=["2025-02-01"]),
        date_to: date = Query(examples=["2025-02-10"]),
):
    rooms = await RoomsService(db).get_rooms_filtered_by_time(hotel_id, date_from, date_to)
    return {"Status": "OK", "data": rooms}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить конкретный отель по ID")
async def get_room(
        hotel_id: int, room_id: int, db: DatabaseDep
):
    try:
        await HotelsService(db).get_one_hotel_by_id(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        return RoomsService(db).get_one_room_by_id(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


# Эндпоинт создания нового номера
@router.post("/{hotel_id}/rooms", summary="Создать новый номер")
async def create_room(
        hotel_id: int, db: DatabaseDep, room_data: RoomAddRequestSchema = Body()
):
    try:
        room = await RoomsService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"Status": "OK", "data": room}


# Эндпоинт для полного изменения номера отеля
@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить информацию о номере")
async def put_room(
        hotel_id: int, room_id: int, db: DatabaseDep, room_data: RoomAddRequestSchema
):
    await RoomsService(db).full_edit_room(hotel_id, room_id, room_data)

    return {"Status": "OK"}


# Эндпоинт для частичного или полного изменения номера отеля
@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичная правка отеля")
async def partially_edit_room(
        hotel_id: int, room_id: int, db: DatabaseDep, room_data: RoomPatchRequestSchema
):
    await RoomsService(db).partially_edit_room(hotel_id, room_id, room_data)

    return {"Status": "OK"}


# Эндпоинт для удаления номера
@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление отеля")
async def delete_room(
        hotel_id: int, room_id: int, db: DatabaseDep
):
    await RoomsService(db).delete_room(hotel_id, room_id)

    return {"Status": "OK"}
