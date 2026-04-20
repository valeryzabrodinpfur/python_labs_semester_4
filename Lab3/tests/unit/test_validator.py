import pytest
from app.core.models import Transaction
from app.core.exceptions import ValidationError, CurrencyMismatchError
from app.services.validator import validate_transaction


class TestValidateTransaction:

    @pytest.mark.parametrize("id_val, amount_val, category_val, date_val, currency_val, expected_exception", [
        # Валидные случаи
        ("tx1", 100.0, "Books", "2025-01-01", "RUB", None),
        ("tx2", 0.01, "Food", "2025-01-01", "RUB", None),
        ("tx3", 9999999.99, "Tech", "2025-01-01", "RUB", None),

        # Отрицательная сумма
        ("tx4", -10.0, "Books", "2025-01-01", "RUB", ValidationError),
        # Нулевая сумма
        ("tx5", 0.0, "Books", "2025-01-01", "RUB", ValidationError),
        # Пустой ID
        ("", 100.0, "Books", "2025-01-01", "RUB", ValidationError),
        # Пустая категория
        ("tx6", 100.0, "", "2025-01-01", "RUB", ValidationError),
        # Пустая дата
        ("tx7", 100.0, "Books", "", "RUB", ValidationError),
        # Неверная валюта (ожидается RUB)
        ("tx8", 100.0, "Books", "2025-01-01", "USD", CurrencyMismatchError),
        # ID только пробелы
        ("   ", 100.0, "Books", "2025-01-01", "RUB", ValidationError),
        # Категория только пробелы
        ("tx9", 100.0, "   ", "2025-01-01", "RUB", ValidationError),
        # Все поля корректны, но сумма - строка (должна быть отловлена при создании объекта,
        # здесь мы тестируем только валидатор с уже созданным объектом)
    ])
    def test_validate_transaction_parametrized(self, id_val, amount_val, category_val, date_val, currency_val,
                                               expected_exception):
        tx = Transaction(id=id_val, amount=amount_val, category=category_val, date=date_val, currency=currency_val)

        if expected_exception is None:
            # Не должно выбрасывать исключений
            validate_transaction(tx, expected_currency="RUB")
        else:
            with pytest.raises(expected_exception):
                validate_transaction(tx, expected_currency="RUB")

    def test_currency_mismatch_custom_message(self):
        tx = Transaction(id="tx", amount=100.0, category="Test", date="2025-01-01", currency="EUR")
        with pytest.raises(CurrencyMismatchError, match="Ожидалась валюта RUB, получена EUR"):
            validate_transaction(tx, expected_currency="RUB")