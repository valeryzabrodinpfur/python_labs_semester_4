from typing import Iterator, Callable, TypeVar, Optional
import logging
from app.core.models import Transaction
from app.core.exceptions import ValidationError
from app.services.validator import validate_transaction

T = TypeVar('T')
logger = logging.getLogger(__name__)


def filter_valid_transactions(
    transactions: Iterator[Transaction],
    expected_currency: str = "RUB",
    on_error: Optional[Callable[[Transaction, Exception], None]] = None
) -> Iterator[Transaction]:
    """
    Генератор, который пропускает только валидные транзакции.
    Невалидные логирует и отбрасывает.
    """
    for tx in transactions:
        try:
            validate_transaction(tx, expected_currency)
            yield tx
        except ValidationError as e:
            logger.warning(
                f"Пропущена невалидная транзакция id={tx.id}: {e}"
            )
            if on_error is not None:
                on_error(tx, e)
        except Exception as e:
            logger.error(
                f"Неожиданная ошибка при валидации {tx.id}: {e}"
            )
            if on_error is not None:
                on_error(tx, e)


def parse_and_validate_stream(
    file_path: str,
    reader,
    expected_currency: str = "RUB"
) -> Iterator[Transaction]:
    """Объединяет чтение и валидацию в один конвейер."""
    raw_transactions = reader.read(file_path)
    return filter_valid_transactions(raw_transactions, expected_currency)
