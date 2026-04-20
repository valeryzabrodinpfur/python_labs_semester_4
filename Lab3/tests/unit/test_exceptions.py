from app.core.models import Transaction


def test_transaction_normalization():
    """Убедимся, что пробелы в категории, ID, дате и валюте удаляются."""
    tx = Transaction(
        id="  id123  ", amount=100.0,
        category="  Books  ", date=" 2025-01-01 ",
        currency=" RUB "
    )
    assert tx.id == "id123"
    assert tx.category == "Books"
    assert tx.date == "2025-01-01"
    assert tx.currency == "RUB"
