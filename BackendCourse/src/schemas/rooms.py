from pydantic import BaseModel, Field, ConfigDict


class RoomAddSchema(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int
    # hotel_id: int


class RoomSchema(RoomAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchSchema(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
