from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAddRequestSchema(BaseModel):
    date_from: date
    date_to: date


class BookingAddSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingSchema(BookingAddSchema):
    # id: int
    users_id: int
    price: int

    model_config = ConfigDict(from_attributes=True)




