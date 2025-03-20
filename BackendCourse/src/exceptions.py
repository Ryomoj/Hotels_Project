from datetime import date

from fastapi import HTTPException


class BookingsException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingsException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(BookingsException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BookingsException):
    detail = "Не осталось свободных номеров"


class BookingsHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(BookingsHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BookingsHTTPException):
    status_code = 404
    detail = "Номер не найден"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата выезда не может быть раньше даты заезда")
