from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelSchema, HotelPatchSchema, HotelAddSchema

router = APIRouter(prefix='/hotels', tags=['Отели'])


# Эндпоинт получения существующего отеля или отелей
@router.get('', summary='Получить отель или все отели')
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description='Адрес отеля'),
        title: str | None = Query(None, description='Название отеля'),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1))


@router.get('/hotel_id', summary='Получить конкретный отель по ID')
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


# Эндпоинт создания нового отеля
@router.post('', summary='Создать новый отель')
async def create_hotel(hotel_data: HotelAddSchema = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'Отель 5 звезд у моря',
        'location': 'город Сочи, у. Моря, 2'
    }},
    '2': {'summary': 'Дубаи', 'value': {
        'title': 'Отель у фонтана',
        'location': 'город Дубаи, ул. Шейха, 1'
    }}
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {'Status': 'OK', 'data': hotel}


# Эндпоинт для полного изменения отеля
@router.put('/{hotel_id}', summary='Изменить информацию об отеле')
async def put_hotel(hotel_id: int, hotel_data: HotelAddSchema):

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {'Status': 'OK'}


# Эндпоинт для частичного или полного изменения отеля
@router.patch('/{hotel_id}', summary='Частичная правка отеля')
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPatchSchema):

    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {'Status': 'OK'}


# Эндпоинт для удаления отеля
@router.delete('/{hotel_id}', summary='Удаление отеля')
async def delete_hotel(hotel_id: int):

    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {'Status': 'OK'}
