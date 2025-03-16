
class BookingsException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingsException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BookingsException):
    detail = "Не осталось свободных номеров"


class DatabaseConflictException(BookingsException):
    detail = "Возник конфликт в базе данных"


class DateConflictException(BookingsException):
    detail = "Дата выезда позже даты заезда"
