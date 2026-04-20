import pytest
from pathlib import Path
from app.core.models import Transaction

@pytest.fixture
def sample_valid_transaction() -> Transaction:
    """Фикстура валидной транзакции для повторного использования в тестах."""
    return Transaction(
        id="tx001",
        amount=1500.50,
        category="Electronics",
        date="2025-01-15",
        currency="RUB"
    )

@pytest.fixture
def valid_csv_content() -> str:
    """Строка с корректным содержимым CSV (включая заголовки)."""
    return (
        "id,amount,category,date,currency\n"
        "tx001,1500.50,Electronics,2025-01-15,RUB\n"
        "tx002,300.00,Books,2025-01-16,RUB\n"
    )

@pytest.fixture
def mixed_csv_content() -> str:
    """CSV с одной валидной и двумя невалидными строками."""
    return (
        "id,amount,category,date,currency\n"
        "tx001,1500.50,Electronics,2025-01-15,RUB\n"
        "tx002,-50.00,Groceries,2025-01-17,RUB\n"
        "tx003,200.00,Books,2025-01-18,USD\n"
    )

@pytest.fixture
def sample_transaction_data():
    """Словарь с корректными данными для создания Transaction."""
    return {
        "id": "tx101",
        "amount": 4500.00,
        "category": "Software",
        "date": "2025-02-01",
        "currency": "RUB"
    }