from pydantic import BaseModel, Field


class HotelNEW(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)

