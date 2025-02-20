
from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm
from src.schemas.facilities import FacilitySchema


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = FacilitySchema
