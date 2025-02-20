from pydantic import BaseModel, ConfigDict


class FacilityAddSchema(BaseModel):
    title: str


class FacilitySchema(FacilityAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FacilityPatchSchema(BaseModel):
    title: str | None = None

