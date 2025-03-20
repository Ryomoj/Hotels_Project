from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DatabaseDep
from src.schemas.facilities import FacilityAddSchema
from src.services.facilities import FacilitiesService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


# Эндпоинт получения существующего удобства или удобств
@router.get("", summary="Получить удобство или все удобства")
@cache(expire=10)
async def get_facilities(db: DatabaseDep):
    facilities = await FacilitiesService(db).get_all_facilities()
    return {"Status": "OK", "data": facilities}


# Эндпоинт создания нового удобства
@router.post("/facilities", summary="Создать новое удобство")
async def create_facility(
    db: DatabaseDep,
    facility_data: FacilityAddSchema = Body(
        openapi_examples={
            "1": {"summary": "Wi-Fi", "value": {"title": "Бесплатный Wi-Fi"}},
            "2": {"summary": "Холодильник", "value": {"title": "Холодильник"}},
        }
    ),
):
    facility = await FacilitiesService(db).create_new_facility(facility_data)

    return {"Status": "OK", "data": facility}
