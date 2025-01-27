from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'},
]


# Эндпоинт получения существующего отеля или отелей
@app.get('/hotels')
def get_hotels(
        id: int | None = Query(None, description='Идентификатор отеля'),
        title: str | None = Query(None, description='Название отеля'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


# Эндпоинт создания нового отеля
@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title
    })
    return {'Status': 'OK'}


# Эндпоинт для полного изменения отеля
@app.put('/hotels/{hotel_id}')
def put_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body()
):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel['id']:
            hotel['title'] = title
            hotel['name'] = name
    return hotels


# Эндпоинт для частичного или полного изменения отеля
@app.patch('/hotels/{hotel_id}')
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None)
):
    global hotels
    for hotel in hotels:
        if hotel_id == hotel['id']:
            if title is not None:
                hotel['title'] = title
            if name is not None:
                hotel['name'] = name
    return hotels


# Эндпоинт для удаления отеля
@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'Status': 'OK'}
