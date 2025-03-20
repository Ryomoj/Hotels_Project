from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DatabaseDep
from src.exceptions.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatchSchema, HotelAddSchema
from src.services.hotels import HotelsService

router = APIRouter(prefix="/hotels", tags=["Отели"])


# Эндпоинт получения существующего отеля или отелей
@router.get("", summary="Получить отель или все отели")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DatabaseDep,
    location: str | None = Query(None, description="Адрес отеля"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(examples=["2025-02-01"]),
    date_to: date = Query(examples=["2025-02-10"]),
):
    hotels = await HotelsService(db).get_hotels_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )
    return {"Status": "OK", "data": hotels}


@router.get("/hotel_id", summary="Получить конкретный отель по ID")
async def get_hotel(
    hotel_id: int,
    db: DatabaseDep,
):
    try:
        return await HotelsService(db).get_one_hotel_by_id(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


# Эндпоинт создания нового отеля
@router.post("", summary="Создать новый отель")
async def create_hotel(
    db: DatabaseDep,
    hotel_data: HotelAddSchema = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "location": "город Сочи, у. Моря, 2",
                },
            },
            "2": {
                "summary": "Дубаи",
                "value": {
                    "title": "Отель у фонтана",
                    "location": "город Дубаи, ул. Шейха, 1",
                },
            },
        }
    ),
):
    hotel = await HotelsService(db).create_hotel(hotel_data)
    return {"Status": "OK", "data": hotel}


# Эндпоинт для полного изменения отеля
@router.put("/{hotel_id}", summary="Изменить информацию об отеле")
async def put_hotel(hotel_id: int, hotel_data: HotelAddSchema, db: DatabaseDep):
    await HotelsService(db).full_edit_hotel(hotel_id, hotel_data)
    return {"Status": "OK"}


# Эндпоинт для частичного или полного изменения отеля
@router.patch("/{hotel_id}", summary="Частичная правка отеля")
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatchSchema,
    db: DatabaseDep,
):
    await HotelsService(db).partially_edit_hotel(hotel_id, hotel_data, exclude_unset=True)
    return {"Status": "OK"}


# Эндпоинт для удаления отеля
@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DatabaseDep):
    await HotelsService(db).delete_hotel(hotel_id)
    return {"Status": "OK"}
