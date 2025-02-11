from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomSchema
