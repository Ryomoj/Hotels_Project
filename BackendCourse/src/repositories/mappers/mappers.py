from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import BookingSchema
from src.schemas.facilities import FacilitySchema
from src.schemas.hotels import HotelSchema
from src.schemas.rooms import RoomSchema, RoomWithRelsSchema
from src.schemas.users import UserSchema


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = HotelSchema


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomSchema


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRelsSchema


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = BookingSchema


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = FacilitySchema


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserSchema
