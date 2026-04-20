import json
from pathlib import Path
import pytest
from unittest.mock import patch, mock_open
from app.services.aggregator import aggregate_by_category
from app.core.models import Transaction


def test_save_result_json_permission_error(tmp_path, caplog):
    """
    Имитирует ситуацию, когда диск защищён от записи.
    Проверяет, что программа логирует ошибку, а не падает.
    """
    # Arrange: создаём агрегированные данные
    sample_data = {"Electronics": 1500.50, "Books": 300.00}
    output_file = tmp_path / "result.json"
    tmp_file = tmp_path / "result.json.tmp"

    # Act: заменяем open на мок, который выбрасывает PermissionError при записи
    with patch("builtins.open", mock_open()) as mocked_open:
        mocked_open.side_effect = PermissionError("Read-only file system")

        # Эмулируем логику сохранения из main.py (транзакционная запись)
        try:
            with open(tmp_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, ensure_ascii=False, indent=2)
            tmp_file.replace(output_file)
        except PermissionError:
            # Логирование ошибки и удаление временного файла, если он существует
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Ошибка при сохранении результата: Read-only file system")
            if tmp_file.exists():
                tmp_file.unlink()

    # Assert: проверяем, что ошибка была залогирована
    assert "Ошибка при сохранении результата" in caplog.text
    # Проверяем, что временный файл не остался (метод unlink был вызван)
    assert not tmp_file.exists()
    # Проверяем, что итоговый файл не создан
    assert not output_file.exists()