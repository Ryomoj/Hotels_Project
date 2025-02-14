from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DatabaseDep
from src.schemas.rooms import RoomAddSchema, RoomPatchSchema, RoomAddRequestSchema, RoomPatchRequestSchema

router = APIRouter(prefix='/hotels', tags=['Номера'])


# Эндпоинт получения существующих номеров
@router.get('/{hotel_id}/rooms', summary='Получить все номера')
async def get_rooms(
        hotel_id: int,
        db: DatabaseDep,
        date_from: date = Query(example="2025-02-01"),
        date_to: date = Query(example="2025-02-10")
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get('/{hotel_id}/rooms/{room_id}', summary='Получить конкретный отель по ID')
async def get_room(
        hotel_id: int,
        room_id: int,
        db: DatabaseDep
):
    return await db.rooms.get_one_or_none(
        id=room_id,
        hotel_id=hotel_id
    )


# Эндпоинт создания нового номера
@router.post('/{hotel_id}/rooms', summary='Создать новый номер')
async def create_room(
        hotel_id: int,
        db: DatabaseDep,
        room_data: RoomAddRequestSchema = Body(openapi_examples={
            '1': {'summary': 'Номер для двоих', 'value': {
                'title': 'Номер для двоих',
                'description': 'Романтичный номер с видом на океан',
                'price': '4500',
                'quantity': '8'
            }},
            '2': {'summary': 'Номер семейный', 'value': {
                'title': 'Номер семейный',
                'description': 'Просторный и удобный номер рядом с выходом к бассейну',
                'price': '7500',
                'quantity': '4'
            }}
        })):
    _room_data = RoomAddSchema(
        hotel_id=hotel_id,
        **room_data.model_dump()
    )
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {'Status': 'OK', 'data': room}


# Эндпоинт для полного изменения номера отеля
@router.put('/{hotel_id}/rooms/{room_id}', summary='Изменить информацию о номере')
async def put_room(
        hotel_id: int,
        room_id: int,
        db: DatabaseDep,
        room_data: RoomAddRequestSchema
):
    _room_data = RoomAddSchema(
        hotel_id=hotel_id,
        **room_data.model_dump()
    )
    await db.rooms.edit(
        _room_data,
        id=room_id
    )
    await db.commit()
    return {'Status': 'OK'}


# Эндпоинт для частичного или полного изменения номера отеля
@router.patch('/{hotel_id}/rooms/{room_id}', summary='Частичная правка отеля')
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        db: DatabaseDep,
        room_data: RoomPatchRequestSchema
):
    _room_data = RoomPatchSchema(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        id=room_id,
        hotel_id=hotel_id
    )
    await db.commit()
    return {'Status': 'OK'}


# Эндпоинт для удаления номера
@router.delete('/{hotel_id}/rooms/{room_id}', summary='Удаление отеля')
async def delete_room(
        hotel_id: int,
        room_id: int,
        db: DatabaseDep
):
    await db.rooms.delete(
        id=room_id,
        hotel_id=hotel_id
    )
    await db.commit()
    return {'Status': 'OK'}
