from fastapi import Query, APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.hotels import HotelPatchSchema, HotelAddSchema
from src.schemas.rooms import RoomAddSchema, RoomPatchSchema

router = APIRouter(prefix='/hotels', tags=['Номера'])


# Эндпоинт получения существующих номеров
@router.get('/{hotel_id}/rooms', summary='Получить отель или все отели')
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


# @router.get('/hotel_id', summary='Получить конкретный отель по ID')
# async def get_hotel(hotel_id: int):
#     async with async_session_maker() as session:
#         return await HotelsRepository(session).get_one_or_none(id=hotel_id)


# Эндпоинт создания нового номера
@router.post('/{hotel_id}', summary='Создать новый номер')
async def create_room(hotel_id: int, room_data: RoomAddSchema = Body(openapi_examples={
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
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data, hotel_id=hotel_id)
        await session.commit()

    return {'Status': 'OK', 'data': room}


# Эндпоинт для полного изменения номера отеля
@router.put('/{hotel_id}/rooms/{room_id}', summary='Изменить информацию о номере')
async def put_room(hotel_id: int, room_id: int, room_data: RoomAddSchema):

    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {'Status': 'OK'}


# Эндпоинт для частичного или полного изменения номера отеля
@router.patch('/{hotel_id}/rooms/{room_id}', summary='Частичная правка отеля')
async def partially_edit_hotel(hotel_id: int, room_id: int, room_data: RoomPatchSchema):

    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {'Status': 'OK'}


# Эндпоинт для удаления номера
@router.delete('/{hotel_id}/rooms/{room_id}', summary='Удаление отеля')
async def delete_hotel(hotel_id: int, room_id: int):

    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

    return {'Status': 'OK'}
