import pytest
from app.core.models import Transaction


def test_transaction_creation_with_invalid_amount_string():
    """Проверка, что при невалидном amount выбрасывается ValueError."""
    with pytest.raises(ValueError):
        Transaction(
            id="tx", amount="not_a_number",
            category="Test", date="2025-01-01"
        )


def test_transaction_normalization():
    """Убедимся, что пробелы в категории и ID удаляются."""
    tx = Transaction(
        id="  id123  ", amount=100.0,
        category="  Books  ", date="2025-01-01"
    )
    assert tx.id == "id123"
    assert tx.category == "Books"
