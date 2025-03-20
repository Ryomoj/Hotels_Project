from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DatabaseDep
from src.exceptions import ObjectNotFoundException, check_date_to_after_date_from, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatchSchema, HotelAddSchema

router = APIRouter(prefix="/hotels", tags=["Отели"])


# Эндпоинт получения существующего отеля или отелей
@router.get("", summary="Получить отель или все отели")
# @cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DatabaseDep,
    location: str | None = Query(None, description="Адрес отеля"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(examples=["2025-02-01"]),
    date_to: date = Query(examples=["2025-02-10"]),
):
    check_date_to_after_date_from(date_from, date_to)
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/hotel_id", summary="Получить конкретный отель по ID")
async def get_hotel(
    hotel_id: int,
    db: DatabaseDep,
):
    try:
        return await db.hotels.get_one(id=hotel_id)
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"Status": "OK", "data": hotel}


# Эндпоинт для полного изменения отеля
@router.put("/{hotel_id}", summary="Изменить информацию об отеле")
async def put_hotel(hotel_id: int, hotel_data: HotelAddSchema, db: DatabaseDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"Status": "OK"}


# Эндпоинт для частичного или полного изменения отеля
@router.patch("/{hotel_id}", summary="Частичная правка отеля")
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPatchSchema,
    db: DatabaseDep,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"Status": "OK"}


# Эндпоинт для удаления отеля
@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DatabaseDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"Status": "OK"}
