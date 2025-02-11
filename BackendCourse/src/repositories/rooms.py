from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import RoomSchema, RoomAddSchema


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomSchema

    async def get_all(self, hotel_id: int) -> list[RoomSchema]:
        query = select(RoomsOrm).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)

        return [RoomSchema.model_validate(room, from_attributes=True) for room in result.scalars().all()]

    async def add(self, data: RoomAddSchema, **hotel_id: int):
        add_data_stmt = insert(RoomsOrm).values(**data.model_dump(), **hotel_id).returning(RoomsOrm)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()

        return self.schema.model_validate(model)
