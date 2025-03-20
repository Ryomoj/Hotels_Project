from src.schemas.facilities import FacilityAddSchema
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilitiesService(BaseService):
    async def get_all_facilities(
            self
    ):
        return await self.db.facilities.get_all()

    async def create_new_facility(
            self, data: FacilityAddSchema
    ):
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()
        return facility
