from datetime import date

from fastapi import HTTPException


class BookingsException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingsException):
    detail = "Объект не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class NoRoomsForBookingException(ObjectNotFoundException):
    detail = "Комнат для бронирования не найдено"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Комната не найдена"


class ObjectAlreadyExistsException(BookingsException):
    detail = "Объект уже существует"


class IncorrectTokenException(BookingsException):
    detail = "Некорректный токен"


class EmailIsNotRegisteredException(BookingsException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(BookingsException):
    detail = "Неверный пароль"


class UserAlreadyExistsException(BookingsException):
    detail = "Пользователь уже существует"


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


class NoRoomsForBookingFoundHTTPException(BookingsHTTPException):
    status_code = 404
    detail = "На эти даты не осталось комнат"


class IncorrectTokenHTTPException(BookingsHTTPException):
    status_code = 404
    detail = "Неверный токен"


class EmailIsNotRegisteredHTTPException(BookingsHTTPException):
    status_code = 404
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordHTTPException(BookingsHTTPException):
    status_code = 404
    detail = "Неверный пароль"


class UserEmailAlreadyExistsHTTPException(BookingsHTTPException):
    status_code = 409
    detail = "Такой email уже зарегистрирован"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата выезда не может быть раньше даты заезда")


