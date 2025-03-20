from datetime import date

from src.exceptions.exceptions import (
    check_date_to_after_date_from, ObjectNotFoundException,
    HotelNotFoundException, RoomNotFoundException)
from src.schemas.facilities import RoomFacilityAddSchema
from src.schemas.rooms import RoomAddRequestSchema, RoomAddSchema, RoomPatchSchema, RoomPatchRequestSchema, RoomSchema
from src.services.base import BaseService
from src.services.hotels import HotelsService


class RoomsService(BaseService):

    async def get_rooms_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to
        )

    async def get_one_room_by_id(
            self,
            hotel_id: int,
            room_id: int
    ):
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(
            self,
            hotel_id: int,
            data: RoomAddRequestSchema
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as exc:
            raise HotelNotFoundException from exc
        _room_data = RoomAddSchema(hotel_id=hotel_id, **data.model_dump())
        room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilityAddSchema(room_id=room.id, facility_id=f_id)
            for f_id in data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def full_edit_room(
            self,
            hotel_id: int,
            room_id: int,
            data: RoomAddRequestSchema
    ):
        await HotelsService(self.db).check_is_hotel_exists(hotel_id)
        await self.check_is_room_exists(room_id)
        _room_data = RoomAddSchema(hotel_id=hotel_id, **data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(room_id, facilities_ids=data.facilities_ids)
        await self.db.commit()

    async def partially_edit_room(
            self,
            hotel_id: int,
            room_id: int,
            data: RoomPatchRequestSchema
    ):
        await HotelsService(self.db).check_is_hotel_exists(hotel_id)
        await self.check_is_room_exists(room_id)
        _data_dict = data.model_dump(exclude_unset=True)
        _data = RoomPatchSchema(hotel_id=hotel_id, **_data_dict)
        await self.db.rooms.edit(_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in _data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facilities_ids=_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(
            self,
            hotel_id: int,
            room_id: int
    ):
        await HotelsService(self.db).check_is_hotel_exists(hotel_id)
        await self.check_is_room_exists(room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def check_is_room_exists(self, room_id) -> RoomSchema:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

