from datetime import date

from src.exceptions.exceptions import check_date_to_after_date_from, ObjectNotFoundException, \
    HotelNotFoundHTTPException, HotelNotFoundException
from src.schemas.hotels import HotelAddSchema, HotelPatchSchema, HotelSchema
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_hotels_filtered_by_time(
            self,
            pagination,
            location: str | None,
            title: str | None,
            date_from: date,
            date_to: date
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_one_hotel_by_id(
            self,
            hotel_id: int,
    ):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, data: HotelAddSchema):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def full_edit_hotel(self, hotel_id: int, data: HotelAddSchema):
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def partially_edit_hotel(self, hotel_id: int, data: HotelPatchSchema):
        await self.db.hotels.edit(data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int,):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def check_is_hotel_exists(self, hotel_id) -> HotelSchema:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
