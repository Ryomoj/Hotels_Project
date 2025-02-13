from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = HotelSchema

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> list[HotelSchema]:
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))

        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)

        return [HotelSchema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    # async def add(self, hotels_data):
    #
    #     add_hotel_stmt = insert(HotelsOrm).values(hotels_data.model_dump())
    #
    #     await self.session.execute(add_hotel_stmt)


