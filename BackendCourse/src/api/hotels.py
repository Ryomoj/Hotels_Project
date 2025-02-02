from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelNEW, HotelPATCH

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
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.like(f"%{location}%"))

        if title:
            query = query.filter(HotelsOrm.title.like(f"%{title}%"))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        result = await session.execute(query)

        hotels = result.scalars().all()
        # print(type(hotels), hotels)
        return hotels


# Эндпоинт создания нового отеля
@router.post('', summary='Создать новый отель')
async def create_hotel(hotel_data: HotelNEW = Body(openapi_examples={
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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={'literal_binds': True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {'Status': 'OK'}


# Эндпоинт для полного изменения отеля
@router.put('/{hotel_id}', summary='Изменить информацию об отеле')
def put_hotel(hotel_id: int, hotel_data: HotelNEW):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel['id']:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
    return hotels


# Эндпоинт для частичного или полного изменения отеля
@router.patch('/{hotel_id}', summary='Частичная правка отеля')
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel['id']:
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            if hotel_data.name is not None:
                hotel['name'] = hotel_data.name
    return hotels


# Эндпоинт для удаления отеля
@router.delete('/{hotel_id}', summary='Удаление отеля')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'Status': 'OK'}
