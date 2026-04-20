class BaseAppError(Exception):
    """Базовое исключение для всего приложения."""
    pass


class DataFormatError(BaseAppError):
    """Ошибка структуры файла (например, не удалось распарсить CSV/JSON)."""
    pass


class ValidationError(BaseAppError):
    """Ошибка бизнес-логики (невалидные данные в транзакции)."""
    pass


class CurrencyMismatchError(ValidationError):
    """Обнаружены разные валюты без конвертации (бонус)."""
    pass


class DuplicateTransactionIdError(ValidationError):
    """Повторяющийся id транзакции в рамках одного источника."""
    pass