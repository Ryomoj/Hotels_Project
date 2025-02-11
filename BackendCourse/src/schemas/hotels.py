from pydantic import BaseModel, Field, ConfigDict


class HotelAddSchema(BaseModel):
    title: str
    location: str


class HotelSchema(HotelAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HotelPatchSchema(BaseModel):
    title: str | None = None
    location: str | None = None

