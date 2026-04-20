import pytest
from app.io.csv_reader import CSVReader
from app.services.validator import validate_transaction
from app.services.aggregator import aggregate_stream
from app.core.exceptions import DataFormatError


def test_csv_reader_with_tmp_path(tmp_path, mixed_csv_content):
    """Создаёт временный CSV, читает, валидирует и проверяет агрегацию."""
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(mixed_csv_content, encoding='utf-8')

    reader = CSVReader()
    raw_transactions = list(reader.read(str(csv_file)))

    valid_txs = []
    for tx in raw_transactions:
        try:
            validate_transaction(tx, expected_currency="RUB")
            valid_txs.append(tx)
        except Exception:
            pass

    assert len(valid_txs) == 1
    assert valid_txs[0].id == "tx001"
    assert valid_txs[0].amount == 1500.50
    assert valid_txs[0].currency == "RUB"

    aggregated = aggregate_stream(iter(valid_txs))
    expected = {"Electronics": 1500.50}
    assert aggregated == expected


def test_csv_reader_empty_file(tmp_path):
    """Проверка обработки пустого CSV."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text(
        "id,amount,category,date,currency\n", encoding='utf-8'
    )

    reader = CSVReader()
    transactions = list(reader.read(str(empty_file)))
    assert transactions == []


def test_csv_reader_missing_columns(tmp_path):
    """Проверка выбрасывания DataFormatError при отсутствии колонок."""
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text(
        "id,amount,date\n1,100,2025-01-01\n", encoding='utf-8'
    )

    reader = CSVReader()
    with pytest.raises(
        DataFormatError, match="Отсутствуют обязательные колонки"
    ):
        list(reader.read(str(bad_csv)))
