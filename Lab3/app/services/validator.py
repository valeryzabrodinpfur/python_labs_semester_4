from app.core.models import Transaction
from app.core.exceptions import ValidationError, CurrencyMismatchError


def validate_transaction(
    tx: Transaction, expected_currency: str = "RUB"
) -> None:
    """
    Проверяет бизнес-правила для одной транзакции.
    - amount > 0
    - id не пустой
    - category не пустая
    - date не пустая
    - валюта соответствует ожидаемой (опционально)
    """
    if not tx.id:
        raise ValidationError("Пустой идентификатор транзакции")
    if tx.amount <= 0:
        raise ValidationError(
            f"Сумма должна быть положительной (получено {tx.amount})"
        )
    if not tx.category:
        raise ValidationError("Категория не может быть пустой")
    if not tx.date:
        raise ValidationError("Дата не может быть пустой")

    if expected_currency and tx.currency != expected_currency:
        raise CurrencyMismatchError(
            f"Ожидалась валюта {expected_currency}, "
            f"получена {tx.currency}"
        )
