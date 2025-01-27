from fastapi import Query, APIRouter, Body

from schemas.hotels import HotelNEW, HotelPATCH

router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'},
    {'id': 3, 'title': 'Spain', 'name': 'siesta'},
    {'id': 4, 'title': 'Italy', 'name': 'italia'},
    {'id': 5, 'title': 'United States', 'name': 'usa'},
    {'id': 6, 'title': 'Saint-Petesrburg', 'name': 'spb'},
    {'id': 7, 'title': 'Moscow', 'name': 'msk'}
]


# Эндпоинт получения существующего отеля или отелей
@router.get('', summary='Получить отель или все отели')
def get_hotels(
        id: int | None = Query(None, description='Айдишник'),
        title: str | None = Query(None, description='Название отеля'),
        page: int | None = Query(1),
        per_page: int | None = Query(7)
):

    hotels_ = []

    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)

    min_offset = (page - 1) * per_page
    max_offset = page * per_page

    return hotels_[min_offset:max_offset]


# Эндпоинт создания нового отеля
@router.post('', summary='Создать новый отель')
def create_hotel(hotel_data: HotelNEW = Body(openapi_examples={
    '1': {'summary': 'Сочи', 'value': {
        'title': 'Отель Сочи 5 звезд у моря',
        'name': 'sochi_u_morya'
    }},
    '2': {'summary': 'Дубаи', 'value': {
        'title': 'Отель Дубаи у фонтана',
        'name': 'dubai_u_fontana'
    }}
})):

    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })
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
