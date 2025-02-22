from fastapi import APIRouter, Body

from src.api.dependencies import DatabaseDep
from src.schemas.facilities import FacilityAddSchema

router = APIRouter(prefix='/facilities', tags=['Удобства'])


# Эндпоинт получения существующего удобства или удобств
@router.get('', summary='Получить удобство или все удобства')
async def get_facilities(
        db: DatabaseDep,
):
    return await db.facilities.get_all()


# Эндпоинт создания нового удобства
@router.post('/facilities', summary='Создать новое удобство')
async def create_facility(
        db: DatabaseDep,
        facility_data: FacilityAddSchema = Body(openapi_examples={
            '1': {'summary': 'Wi-Fi', 'value': {
                'title': 'Бесплатный Wi-Fi'
            }},
            '2': {'summary': 'Холодильник', 'value': {
                'title': 'Холодильник'
            }}
        })):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {'Status': 'OK', 'data': facility}
