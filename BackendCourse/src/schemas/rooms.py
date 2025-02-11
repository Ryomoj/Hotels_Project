from pydantic import BaseModel, Field, ConfigDict


class RoomAddRequestSchema(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomAddSchema(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomSchema(RoomAddSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequestSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatchSchema(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
