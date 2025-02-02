from src.repositories.base import BaseRepository
from src.models.hotels import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    